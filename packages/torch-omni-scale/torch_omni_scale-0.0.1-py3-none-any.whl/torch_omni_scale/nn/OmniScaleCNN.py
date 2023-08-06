import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_omni_scale.utils.omniscale_utils import *

    
class build_layer_with_layer_parameter(nn.Module):
    def __init__(self,layer_parameters):
        super(build_layer_with_layer_parameter, self).__init__()

        os_mask, init_weight, init_bias= creak_layer_mask(layer_parameters)
        
        
        in_channels = os_mask.shape[1]
        out_channels = os_mask.shape[0]
        max_kernel_size = os_mask.shape[-1]

        self.weight_mask = nn.Parameter(torch.from_numpy(os_mask),requires_grad=False)
        
        self.padding = nn.ConstantPad1d((int((max_kernel_size-1)/2), int(max_kernel_size/2)), 0)
         
        self.conv1d = torch.nn.Conv1d(in_channels=in_channels, out_channels=out_channels, kernel_size=max_kernel_size)
        self.conv1d.weight = nn.Parameter(torch.from_numpy(init_weight),requires_grad=True)
        self.conv1d.bias =  nn.Parameter(torch.from_numpy(init_bias),requires_grad=True)

        self.bn = nn.BatchNorm1d(num_features=out_channels)
    
    def forward(self, X):
        self.conv1d.weight.data = self.conv1d.weight*self.weight_mask
        #self.conv1d.weight.data.mul_(self.weight_mask)
        result_1 = self.padding(X)
        result_2 = self.conv1d(result_1)
        result_3 = self.bn(result_2)
        result = F.relu(result_3)
        return result 
    
class OmniScaleCNN(nn.Module):
    def __init__(self,len_ts,input_channel,n_class,paramenter_number_of_layer_list):
        super(OmniScaleCNN, self).__init__()
        start_kernel_size = 1
        Max_kernel_size = 89
        self.layer_parameter_list = generate_layer_parameter_list(start_kernel_size,
                                                    min(int(len_ts/4),Max_kernel_size),
                                                    paramenter_number_of_layer_list,
                                                    in_channel = input_channel)
        self.layer_list = []
        
        
        for i in range(len(self.layer_parameter_list)):
            layer = build_layer_with_layer_parameter(self.layer_parameter_list[i])
            self.layer_list.append(layer)
        
        self.net = nn.Sequential(*self.layer_list)
            
        self.averagepool = nn.AdaptiveAvgPool1d(1)
        
        out_put_channel_numebr = 0
        for final_layer_parameters in self.layer_parameter_list[-1]:
            out_put_channel_numebr = out_put_channel_numebr+ final_layer_parameters[1] 
            
        self.hidden = nn.Linear(out_put_channel_numebr, n_class)

    def forward(self, X):
        X = X.permute(0,2,1)
        X = X.float()
        X = self.net(X)
        X = self.averagepool(X)
        X = X.squeeze_(-1)
        X = self.hidden(X)
        return X
        
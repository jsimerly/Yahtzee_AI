import torch
import numpy as np

class YahtzeeModel(torch.nn.Module):
    def __init__(self, state_dim_dice, action_dim_dice, action_dim_score):
        super(YahtzeeModel, self).__init__()
        self.fc_dice = torch.nn.Linear(state_dim_dice, 128)
        self.fc_score = torch.nn.Linear(state_dim_dice, 128)
        self.fc_out_dice = torch.nn.Linear(128, action_dim_dice)
        self.fc_out_score = torch.nn.Linear(128, action_dim_score)

    def forward(self, state, state_type):
        if state_type == 'dice':
            x = torch.relu(self.fc_dice(state))
            x = self.fc_out_dice(x)
        elif state_type == 'score':
            x = torch.relu(self.fc_score(state))
            x = self.fc_out_score(x)
        return x
    

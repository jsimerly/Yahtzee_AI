from numpy.typing import NDArray
import torch
from torch import nn, optim
import numpy as np
from base import YahtzeeModel


class FirstModel(nn.Module, YahtzeeModel):
    def __init__(self, input_size: int, hidden_size: int = 64, hold_output_size: int = 5, score_output_size: int = 13):
        super(YahtzeeModel, self).__init__()

        self.hold_network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hold_output_size),
            nn.Sigmoid()
        )

        self.score_network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, score_output_size)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.hold_loss_fn = nn.BCELoss()
        self.score_loss_fn = nn.MSELoss()

    def forward_hold(self, x: torch.Tensor) -> torch.Tensor:
        return self.hold_network(x)
    
    def forward_score(self, x: torch.Tensor) -> torch.Tensor:
        return self.score_network(x)
    
    def decide_dice_holds(self, state: np.ndarray) -> np.ndarray:
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state)
            probabilities = self.forward_hold(state_tensor)
            return (probabilities > 0.5).cpu().numpy().astype(int)

    def decice_scoring(self, state: np.ndarray) -> int:
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state)
            scores = self.forward_score(state_tensor)
            return scores.argmax.item()
        
    def train_on_turn(self,
        hold_states: list[NDArray], 
        hold_decisions: list[NDArray], 
        final_state: list[NDArray], 
        score_category: int, 
        turn_score: int
    ) -> float:
        #train on hold decisions
        hold_states_tensor = torch.FloatTensor(np.array(hold_states))
        hold_decisions_tensor = torch.FloatTensor(np.array(hold_decisions))

        hold_probs = self.forward_hold(hold_states_tensor)
        hold_loss = self.hold_loss_fn(hold_probs, hold_decisions_tensor) * -turn_score

        #train on scoring decision
        final_state_tensor = torch.FloatTensor(final_state)
        score_predictions = self.forward_score(final_state_tensor)
        target_scores = torch.zeros_like(score_predictions)
        target_scores[score_category] = turn_score
        score_loss = self.score_loss_fn(score_predictions, target_scores)

        total_loss = hold_loss + score_loss

        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

    def train_on_game(self, 
        states: list[NDArray], 
        hold_decisions: list[NDArray], 
        score_decisions: list[NDArray], 
        scores: list[int], 
        final_scores: int
    ) -> float:
        states_tensor = torch.FloatTensor(np.array(states))
        hold_decisions_tensor = torch.FloatTensor(np.array(hold_decisions))
        
        hold_probs = self.forward_hold(states_tensor)
        hold_loss = self.hold_loss_fn(hold_probs, hold_decisions_tensor) * -final_scores

        score_predictions = self.forward_score(states_tensor)
        target_scores = torch.zeros_like(score_predictions)
        for i, (category, score) in enumerate(zip(score_decisions, scores)):
            target_scores[i, category] = score
        score_loss = self.score_loss_fn(score_predictions, target_scores)

        total_loss = hold_loss + score_loss
        
        self.optimizer.zero_grad()
        total_loss.backward()
        self.optimizer.step()

        

    

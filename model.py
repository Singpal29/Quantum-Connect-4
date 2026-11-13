import engine
import torch
import torch.nn as nn
import torch.nn.functional as F





class Model(nn.Module):
  def __init__(self, rows, cols, channels = 64):
    super().__init__()

    self.conv1 = nn.Conv2d(6, channels, kernel_size=3, padding=1)
    self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
    self.conv3 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)

    flat_size = channels * rows * cols

    num_actions = cols + cols * rows + (cols * (cols + 1)) // 2

    self.policy_fc = nn.Linear(flat_size, num_actions)

    self.value_fc1 = nn.Linear(flat_size, 64)
    self.value_fc2 = nn.Linear(64, 1)

  def forward(self, x):
    x = self.conv1(x)
    x = F.relu(x)
    x = self.conv2(x)
    x = F.relu(x)
    x = self.conv3(x)
    x = F.relu(x)

    x = torch.flatten(x, 1)

    policy = self.policy_fc(x)

    value = self.value_fc1(x)
    value = F.relu(value)
    value = self.value_fc2(value)
    value = torch.tanh(value)

    return policy, value

def main():
  game = engine.Game()
  x = torch.tensor(game.encode(), dtype=torch.float32)   # shape (6, rows, cols)
  x = x.unsqueeze(0)                                     # add batch dim → (1, 6, rows, cols)

  net = Model(engine.rows, engine.cols)
  policy, value = net(x)
  print(policy)
  print(value)

if __name__ == "__main__":
  main()


  

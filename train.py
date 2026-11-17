import collections
import random
import time
import qc4.MCTS as MCTS
import qc4.az_MCTS as az_MCTS
import qc4.model as model
import qc4.selfplay as selfplay
import qc4.engine as engine
import torch
import pandas as pd
import pickle
import os
import config


def train_step(batch, net, optimizer):
  states, policies, outcomes = zip(*batch)
  states = torch.tensor(states, dtype=torch.float32)
  policies = torch.tensor(policies, dtype=torch.float32)
  outcomes = torch.tensor(outcomes, dtype=torch.float32)
  outcomes = outcomes.unsqueeze(1)
  policy, value = net(states)
  value_loss = ((value - outcomes) ** 2).mean()
  policy_loss = -(policies * torch.log_softmax(policy, dim = 1)).sum(dim = 1).mean()
  loss = value_loss + policy_loss
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()
  return policy_loss.item(), value_loss.item()
  

def generation(net, optimizer, buffer, iterations = 200, games = 25, steps = 200, count = 0):
  
  for i in range(games):
    buffer.extend(selfplay.self_play_game(net, iterations))
  with open(f"runs/run{config.RUN}/buffer_tmp.pkl", "wb") as f:
    pickle.dump(list(buffer), f)
  os.replace(f"runs/run{config.RUN}/buffer_tmp.pkl", f"runs/run{config.RUN}/buffer.pkl")
  policy_losses = []
  value_losses = []
  for i in range(steps):
    policy_loss, value_loss = train_step(random.sample(buffer, min(64, len(buffer))), net, optimizer)
    policy_losses.append(policy_loss)
    value_losses.append(value_loss)

  loss_data = {
    "generation": count,
    "policy_loss_avg": sum(policy_losses) / len(policy_losses),
    "value_losses_avg": sum(value_losses) / len(value_losses)
  }
  torch.save(net.state_dict(), f"runs/run{config.RUN}/generations/gen_{count}.pt")
  torch.save(optimizer.state_dict(), f"runs/run{config.RUN}/optimizer.pt")
  print(f"generation {count} complete")
  return loss_data
  



def main():
  if os.path.isdir(f"runs/run{config.RUN}"):
    cont = input("Warning this could potentially overwrite existing generations, continue anyway? Type an explicit YES to continue")
    if cont != "YES": return
  os.makedirs(f"runs/run{config.RUN}", exist_ok=True)
  os.makedirs(f"runs/run{config.RUN}/generations", exist_ok=True)
  start = time.perf_counter()
  net = model.Model(config.ROWS, config.COLS)
  
  optimizer = torch.optim.Adam(net.parameters(), lr = 1e-3)
  buffer = collections.deque(maxlen = 20000)
  rows = []
  df = pd.DataFrame()
  for i in range(200):
    print(i)
    rows.append(generation(net, optimizer, buffer, games = 50, steps = 200, count = i + 1))
    pd.DataFrame(rows).to_csv(f"runs/run{config.RUN}/training_log.csv", index=False)
    
  
  print(time.perf_counter() - start)
  

if __name__ == "__main__":
  main()

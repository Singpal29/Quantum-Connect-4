import collections
import random
import time

import MCTS
import az_MCTS
import model
import selfplay
import engine
import torch
import pandas as pd
import pickle
import os


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
  with open("buffer_tmp.pkl", "wb") as f:
    pickle.dump(list(buffer), f)
  os.replace("buffer_tmp.pkl", "buffer.pkl")
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
  torch.save(net.state_dict(), f"generations/gen_{count}.pt")
  torch.save(optimizer.state_dict(), f"optimizer.pt")
  print(f"generation {count} complete")
  return loss_data
  
def play_game(net, count = 500, search1 = 500, search2 = 500, swap = False):
  game = engine.Game()
  tracker = 1 if swap else 0
  while game.winner == 0 and tracker < count:
    if tracker % 2 == 0: 
      root = MCTS.Node(game=game.copy())
      game.apply(root.search(search1))
    else: 
      root = az_MCTS.Node(game=game.copy())
      move, visits = root.search(search2, net)
      game.apply(move)
    tracker += 1
  assert game.winner != 0, "Time Out"
  return game.winner

def evaluate(gen_count, df):
  
  net = model.Model(engine.rows, engine.cols)
  net.load_state_dict(torch.load(f"generations/gen_{gen_count}.pt"))
  draws = 0
  az_mcts = [0, 0]
  mcts = [0, 0]
  for i in range(100):
    res = play_game(net, 500, 500, 500, i % 2 == 0)
    if (res == 1): 
      if (i % 2 == 0):
        az_mcts[0] += 1
      else:
        mcts[1] += 1
    elif (res == 2): 
      draws += 1
    else: 
      if (i % 2 == 1):
        az_mcts[1] += 1
      else:
        mcts[0] += 1
  new_row = pd.DataFrame([{
    "Generation": gen_count,
    "Net First": az_mcts[0],
    "Net Second": az_mcts[1],
    "MCTS First": mcts[1],
    "MCTS Second": mcts[0],
    "Draws": draws
  }])
  print(f"Generation: {gen_count}")
  print(az_mcts)
  print(mcts)
  print(draws)
  df = pd.concat([df, new_row], ignore_index=True)
  df.to_csv("results.csv", index = False)
  return df
  

def main():
  start = time.perf_counter()
  net = model.Model(engine.rows, engine.cols)
  optimizer = torch.optim.Adam(net.parameters(), lr = 1e-3)
  buffer = collections.deque(maxlen = 20000)
  rows = []
  df = pd.DataFrame(columns = ["Generation", "Net First", "Net Second", "MCTS First", "MCTS Second", "Draws"])

  for i in range(200):
    print(i)
    rows.append(generation(net, optimizer, buffer, games = 50, steps = 200, count = i + 1))
    pd.DataFrame(rows).to_csv("training_log.csv", index=False)
    if (i % 5 == 0):
      df = evaluate(i + 1, df)
  
  print(time.perf_counter() - start)
  

if __name__ == "__main__":
  main()

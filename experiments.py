import pandas as pd
import qc4.model as model
import torch
import qc4.selfplay as selfplay
import config
import time
import qc4.players as players
import qc4.arena as arena


def first_player_wins(start = 10, end = 200, step = 10, iterations = 100, games = 100):
  start_time = time.perf_counter()
  net = model.Model(config.ROWS, config.COLS)
  df = pd.DataFrame()
  for i in range(start, end + 1, step):
    print(f"Generation {i}")
    
    net = players.load_generation(config.RUN, i)
    first_player = players.NetworkPlayer(net, iterations)
    second_player = players.NetworkPlayer(net, iterations)
    
    #{"a_first": p1_first[0], "a_second": p2_first[0], "b_first": p2_first[1], "b_second": p1_first[1], "draws": draws}
    examples = arena.play_match(first_player, second_player, games, False, False, 5)
    
    print(examples["a_first"])
    print(examples["draws"])
    print(examples["b_second"])
    print(time.perf_counter() - start_time)
    df = pd.concat([df, pd.DataFrame([{
      "Generation": i,
      "First Player": examples["a_first"],
      "Draws": examples["draws"],
      "Second Player": examples["b_second"]
    }])], ignore_index=True)
    
    df.to_csv("results/first_player_random_move.csv", index = False)
      

def main():
  first_player_wins()
  
def evaluate(gen_count1, gen_count2, df, iterations = 500, games = 100):
  print(f"Generation {gen_count1} vs Generation {gen_count2}")
  net1 = players.load_generation(config.RUN, gen_count1)
  net2 = players.load_generation(config.RUN, gen_count2)
  player1 = players.NetworkPlayer(net1, iterations)
  player2 = players.NetworkPlayer(net2, iterations)
  
  row = arena.play_match(player1, player2, games, True, False, 5)
  
  new_row = pd.DataFrame([{
    "Generation 1": gen_count1,
    "Generation 2": gen_count2,
    "Gen 1 First": row["a_first"],
    "Gen 1 Second": row["a_second"],
    "Gen 2 First": row["b_first"],
    "Gen 2 Second": row["b_second"],
    "Draws": row["draws"]
  }])
  print(f"Generation 1: {gen_count2}")
  print(f"Generation 2: {gen_count1}")
  
  df = pd.concat([df, new_row], ignore_index=True)
  df.to_csv("results/pvp.csv", index = False)
  return df
  




if __name__ == "__main__":
  main()


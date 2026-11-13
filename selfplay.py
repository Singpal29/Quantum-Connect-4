import az_MCTS
import engine
import random
import model
import time


def self_play_game(net, iterations, explore_moves = 10):
  root = engine.Game()
  
  encoded = []
  policies = []
  turn = []
  while not root.gameOver:
    mcts = az_MCTS.Node(root.copy())
    move, visit_counts = mcts.search(iterations, net)
    total = sum(visit_counts)
    search_policy = [x / total for x in visit_counts]
    if explore_moves:
      move = random.choices(range(len(search_policy)), weights = search_policy)[0]
      explore_moves -= 1
    encoded.append(root.encode())
    policies.append(search_policy)
    turn.append(root.curr_player)
    root.apply(move)

  examples = []

  for state, policy, player in zip(encoded, policies, turn):
    if root.winner == 2:
      outcome = 0
    elif root.winner == player:
      outcome = 1
    else:
      outcome = -1
    examples.append((state, policy, outcome))
  return examples
  
def main():
  net = model.Model(engine.rows, engine.cols)
  start = time.perf_counter()
  examples = self_play_game(net, 200)
  print(f"time = {time.perf_counter() - start}")
  print(len(examples))
  print(sum(random.choice(examples)[1]))
  print([outcome[2] for outcome in examples])




if __name__ == "__main__":
  main()
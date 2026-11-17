import random
import qc4.engine as engine
import qc4.MCTS as MCTS
import qc4.az_MCTS as az_MCTS
import qc4.model as model
import config
import torch

def load_generation(run, n):
  net = model.Model(config.ROWS, config.COLS)
  net.load_state_dict(torch.load(f"runs/run{run}/generations/gen_{n}.pt"))
  return net

class RandomPlayer:
  def move(self, game):
    return random.choice(game.legal_moves())

class GreedyPlayer:
  def move(self, game):
    curr_player = game.curr_player
    moves = game.legal_moves()
    for i in game.legal_moves():
      tempGame = game.copy()
      tempGame.apply(i)
      if (tempGame.winner == curr_player):
        return i
        
    random.shuffle(moves)
    for move in moves:
      tempGame = game.copy()
      tempGame.apply(move)
      if (tempGame.gameOver): 
        if (tempGame.winner == 2):
          return move
          
        continue

      losing = False
      for j in tempGame.legal_moves():
        tempGame2 = tempGame.copy()
        tempGame2.apply(j)
        if (tempGame2.winner == -1 * curr_player):
          losing = True
          break
      if not losing:
        
        return move
    return moves[0]

class MCTSPlayer:
  def __init__(self, depth = 500, greedy = False):
    self.greedy = greedy
    self.depth = depth
    
  def move(self, game):
    root = MCTS.Node(game=game.copy())
    return root.search(self.depth, self.greedy)

class NetworkPlayer():
  def __init__(self, net, iterations):
    self.net = net
    self.iterations = iterations
  def move(self, game):
    root = az_MCTS.Node(game=game.copy())
    move, visits = root.search(self.net, self.iterations)
    return move

class RawNetworkPlayer():
  def __init__(self, net):
    self.net = net
  def move(self, game):
    priors, _ = az_MCTS.Node(game.copy()).evaluate(self.net)
    return max(priors, key=priors.get)




import math
import random
import model
import torch

import engine

C = 1.5

class Node:
  def __init__(self, game = None, parent = None, move_here = -1, prior = 1.0):
    self.game = engine.Game() if game is None else game
    self.visited = 0
    self.value_sum = 0
    self.parent = parent
    self.children = []
    self.move_here = move_here
    self.prior = prior

  def getQ(self):
    if self.visited == 0: return 0
    return self.value_sum / self.visited

  def getBest(self):
    best_score = float('-inf')
    curr = 0
    best_child = None
    for child in self.children:
      curr += child.getQ() #Exploitation
      curr += C * child.prior * math.sqrt(self.visited) / (1 + child.visited) #Exploration
      if (best_score < curr):
        best_score = curr
        best_child = child
      curr = 0
    return best_child

  def expand(self, priors):
    for move in priors:

      forward_game = self.game.copy()
      forward_game.apply(move)
      child = Node(forward_game, self, move, priors[move])
      self.children.append(child)

  def backpropogate(self, value):
    curr = self
    
    while True:
      value *= -1
      curr.visited += 1
      curr.value_sum += value
      curr = curr.parent
      if (curr is None): break
    
  def search(self, iterations = 500, net = model.Model(engine.rows, engine.cols)):
    
    for i in range(iterations):
      curr = self
      while len(curr.children) > 0 and not curr.game.gameOver:
        curr = curr.getBest()

      if curr.game.gameOver:
        winner = curr.game.winner
        if winner != 2: curr.backpropogate(winner * curr.game.curr_player)
        else: curr.backpropogate(0)

      else:
        priors, value = curr.evaluate(net)
        curr.expand(priors)
        curr.backpropogate(value)
        

    most_visits = -1
    best_child = None
    visit_counts = [0] * (engine.cols + engine.cols * engine.rows + (engine.cols * (engine.cols + 1)) // 2)

    for child in self.children:
      visit_counts[child.move_here] += child.visited
      if (child.visited > most_visits):
        best_child = child
        most_visits = child.visited
    return best_child.move_here, visit_counts

  def evaluate(self, model):
    tensor = torch.tensor(self.game.encode(), dtype = torch.float32)
    tensor = tensor.unsqueeze(0) 
    with torch.no_grad():
      policy, value = model(tensor)
      value = value[0]

      actions = policy.shape[1]
      moves = torch.full((actions,), float('-inf'))
      legal_moves = self.game.legal_moves()
      moves[legal_moves] = policy[0][legal_moves]
      probs = torch.softmax(moves, dim=0)  

      priors = {m: probs[m].item() for m in legal_moves}
      return priors, value.item()


      

'''
def greedy_move(game):
    curr_player = game.curr_player
    moves = game.legal_moves()
    for i in game.legal_moves():
      tempGame = game.copy()
      tempGame.apply(i)
      if (tempGame.winner == curr_player):
        game.apply(i)
        return
    random.shuffle(moves)
    for move in moves:
      tempGame = game.copy()
      tempGame.apply(move)
      if (tempGame.gameOver): 
        if (tempGame.winner == 2):
          game.apply(move)
          return
        continue

      losing = False
      for j in tempGame.legal_moves():
        tempGame2 = tempGame.copy()
        tempGame2.apply(j)
        if (tempGame2.winner == -1 * curr_player):
          losing = True
          break
      if not losing:
        game.apply(move)
        return
    game.apply(moves[0])
'''

def main():
  game = engine.Game(True)
  game.owner_board[5][6] = 1
  game.owner_board[5][5] = 1
  game.owner_board[5][4] = 1
  node = Node(game)
  print(node.search(100)[1])



if __name__ == "__main__":
  main()
  
    






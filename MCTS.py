import math
import random

import engine

C = math.sqrt(2)

class Node:
  def __init__(self, game = None, parent = None, move_here = -1):
    self.game = engine.Game() if game is None else game
    self.visited = 0
    self.wins = 0
    self.parent = parent
    self.children = []
    self.move_here = move_here
    self.untried_moves = self.game.legal_moves()

  def getBest(self):
    best_score = -1
    curr = 0
    best_child = None
    for child in self.children:
      curr += child.wins / child.visited #Exploitation
      curr += C * math.sqrt(math.log(self.visited) / child.visited) #Exploration
      if (best_score < curr):
        best_score = curr
        best_child = child
      curr = 0
    return best_child

  def expand(self):
    if len(self.untried_moves) == 0: return
    move = random.choice(self.untried_moves)
    forward_game = self.game.copy()
    forward_game.apply(move)
    child = Node(forward_game, self, move)
    self.children.append(child)
    self.untried_moves.remove(move)
    return child

  def simulateGreedy(self):
    temp = self.game.copy()
    moves = temp.legal_moves()
    while len(moves) > 0:
      greedy_move(temp)
      moves = temp.legal_moves()
    return temp.winner

  def simulate(self):
      temp = self.game.copy()
      moves = temp.legal_moves()
      while len(moves) > 0:
        temp.apply(random.choice(moves))
        moves = temp.legal_moves()
      return temp.winner

  
    

  def backpropogate(self, winner):
    curr = self
    while True:
      curr.visited += 1
      if (curr.game.curr_player * -1 == winner):
        curr.wins += 1
      elif (winner == 2):
        curr.wins += 0.5
      if (curr.parent is None):
        break
      curr = curr.parent

  def search(self, iterations, greedy = False):
    for i in range(iterations):
      curr = self
      while (len(curr.untried_moves) == 0 and not curr.game.gameOver):
        curr = curr.getBest()

      if len(curr.untried_moves) > 0:
        curr = curr.expand()

      if (greedy):
        winner = curr.simulateGreedy()
      else:
        winner = curr.simulate()
      
      curr.backpropogate(winner)

    most_visits = -1
    best_child = None
    for child in self.children:
      if (child.visited > most_visits):
        best_child = child
        most_visits = child.visited
    return best_child.move_here


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
  
    






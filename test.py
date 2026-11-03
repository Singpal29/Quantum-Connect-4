import random
import engine
import time
import MCTS


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

def trainMCTS():
  root = MCTS.Node()
  root.search()



def random_game(game, swap):
  count = 0 if not swap else 1
  
  while game.winner == 0 and count < 500:
    
    if count % 2 == 0: 
      root = MCTS.Node(game=game.copy())
      #print("MCTS move")
      game.apply(root.search(500))
    else: 
      #print("Random move")
      greedy_move(game)
      #game.apply(random.choice(game.legal_moves()))
    #check_invariants(game)
    count+=1
  assert game.winner != 0, "Time Out"
  return game.winner

def check_invariants(game):
  if game.gameOver or len(game.legal_moves()) == 0:
    assert game.gameOver and len(game.legal_moves()) == 0, "Moves past game end or no moves before game end"
  idMatch = {}
  for r in range(engine.rows):
    for c in range(engine.cols):
      if game.ghost_board[r][c] != -1:
        idMatch[game.ghost_board[r][c]] = idMatch.get(game.ghost_board[r][c], 0) + 1
      if (game.owner_board[r][c] != 0 and r < engine.rows - 1):
        assert game.owner_board[r + 1][c] != 0, "Floating value"
  for value in idMatch.values():
    #print(value)
    assert value == 2, game.print_board()


def main():
  #testMCTS()
  game = engine.Game()
  redWins = 0
  greenWins = 0
  draws = 0
  start = time.perf_counter()
  first_player = [0, 0]
  for i in range(100):
    res = random_game(game, i % 2)
    if (res == 1): 
      redWins += 1
      if (i % 2 == 0):
        first_player[0] += 1
      

    elif (res == 2): 
      draws += 1
    else: 
      greenWins += 1
      if (i % 2 == 1):
        first_player[1] += 1
    game = engine.Game()
  elapsed = time.perf_counter() - start
  print(first_player)
  print(redWins)
  print(greenWins)
  print(draws)
  print(elapsed)
if __name__ == "__main__":
  main()
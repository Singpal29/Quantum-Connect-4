import random

import qc4.engine as engine
import qc4.players as players
import config

def check_invariants(game):
  if game.gameOver or len(game.legal_moves()) == 0:
    assert game.gameOver and len(game.legal_moves()) == 0, "Moves past game end or no moves before game end"
  idMatch = {}
  for r in range(config.ROWS):
    for c in range(config.COLS):
      if game.ghost_board[r][c] != -1:
        idMatch[game.ghost_board[r][c]] = idMatch.get(game.ghost_board[r][c], 0) + 1
      if (game.owner_board[r][c] != 0 and r < config.ROWS - 1):
        assert game.owner_board[r + 1][c] != 0, "Floating value"
  for value in idMatch.values():
    #print(value)
    assert value == 2, f"{game.owner_board}\n{game.ghost_board}"

def play_game(player1, player2, invariants = False, opening = None):
  game = engine.Game()
  if opening:
    for i in opening:
      game.apply(i)
  
  cap = 0
  while not game.gameOver and cap < 500:
    player = player1 if game.curr_player == 1 else player2
    move = player.move(game.copy())
    game.apply(move)
    if (invariants):
      check_invariants(game)
    cap += 1
  assert cap < 500, "Too long game"
  
  return game.winner

def play_match(player1, player2, games = 10, swap = True, invariants = False, opening_moves = 0):
  
  p1_first = [0, 0]
  p2_first = [0, 0]
  draws = 0
  opening = []
  for i in range(games):
    if swap and i % 2 == 1:
      
      winner = play_game(player2, player1, invariants, opening)
      if winner == 1:
        p2_first[1] += 1
      elif winner == -1:
        p2_first[0] += 1
    else:
      temp = engine.Game()
      opening = []
      for j in range(opening_moves):
        move_choice = random.choice(temp.legal_moves())
        temp.apply(move_choice)
        opening.append(move_choice)
      winner = play_game(player1, player2, invariants, opening)
      if winner == 1:
        p1_first[0] += 1
      elif winner == -1:
        p1_first[1] += 1

    if winner == 2: draws += 1
  return {"a_first": p1_first[0], "a_second": p2_first[0], "b_first": p2_first[1], "b_second": p1_first[1], "draws": draws}

    



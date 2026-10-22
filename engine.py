id_tracker = 0
owner_board = []
ghost_board = []
curr_player = 1

def copy():
  pass

def winner():
  pass

def apply(move):
  if (move < 7):
    for r in reversed(range(6)):
      if (owner_board[r][move] == 0):
        owner_board[r][move] = curr_player
        curr_player = -1 * curr_player
        break
  elif move < 49:
    row = (move - 49) // 7
    col = (move - 49) % 7
    id = ghost_board[row][col]
    ghost_board[row][col] = -1
    for r in range(6):
      for c in range(7):
        if move == (r * 7 + c + 7):
          continue
        if (ghost_board[r][c] == id):
          ghost_board[r][c] = -1
          curr_player *= -1
          for k in range(r, 5):
            owner_board[k][c] = owner_board[k + 1][c]


def legal_moves():
  valid_moves = []
  count = 0
  for c in range(7):
    if owner_board[0][c] == 0:
      valid_moves.append(c)
    for r in range(c, 7):
      if c == r and owner_board[1][c] == 0:
        valid_moves.append(49 + (count))
      elif owner_board[0][c] == 0 and owner_board[0][r] == 0:
        valid_moves.append(49 + (count))
      count += 1

  for r in range(6):
    for c in range(7):
      if ghost_board[r][c] != -1:
        valid_moves.append((r * 7 + c) + 7)
  valid_moves.sort()
  for move in valid_moves:
    print(move, end = " ")


def main():
  for r in range(6):
    owner_board.append([0, 0, 0, 0, 0, 0, 0])
    ghost_board.append([-1, -1, -1, -1, -1, -1, -1])
  legal_moves()



if (__name__ == "__main__") :
  main()
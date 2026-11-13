rows = 6
cols = 7

class Game:
  def __init__(self, new = True):
    
    self.owner_board = []
    self.ghost_board = []
    self.curr_player = 1
    self.gameOver = False
    self.winner = 0
    self.id_tracker = 0
    if new:
      for r in range(rows):
        self.owner_board.append([0, 0, 0, 0, 0, 0, 0])
        self.ghost_board.append([-1, -1, -1, -1, -1, -1, -1])
  


  def copy(self):
    copy_game = Game(new = False)
    copy_game.curr_player = self.curr_player
    copy_game.winner = self.winner

    copy_game.curr_player = self.curr_player
    copy_game.id_tracker = self.id_tracker
    copy_game.gameOver = self.gameOver
    copy_game.winner = self.winner
    for r in range(rows):
      copy_game.owner_board.append(list.copy(self.owner_board[r]))
      copy_game.ghost_board.append(list.copy(self.ghost_board[r]))
    return copy_game

  def setWinner(self, winner1, winner2, draw):
    if not (winner1 or winner2 or draw): return
    self.gameOver = True;
    if draw:
      self.winner = 2
    if (winner1 and winner2):
      self.winner = 2
    else:
      if winner2:
        self.winner = -1
      elif winner1:
        self.winner = 1
    

  def checkGame(self):
    draw = True
    winner1 = False
    winner2 = False
    for r in range(rows):
      if (not draw): break
      for c in range(cols):
        if (self.ghost_board[r][c] != -1 or self.owner_board[r][c] == 0): 
          draw = False
          break
    for r in range(rows):
      for c in range(cols - 3):
        if self.owner_board[r][c] != 0 and self.ghost_board[r][c] == -1 :
          if (
            self.owner_board[r][c] == self.owner_board[r][c + 1]
            and self.ghost_board[r][c + 1] == -1 
            and self.owner_board[r][c] == self.owner_board[r][c + 2] 
            and self.ghost_board[r][c + 2] == -1 
            and self.owner_board[r][c] == self.owner_board[r][c + 3] 
            and self.ghost_board[r][c + 3] == -1
          ):
            if (self.owner_board[r][c] == 1):
              winner1 = True
            else:
              winner2 = True
        
    for c in range(cols):
        for r in range(rows - 3):
          if self.owner_board[r][c] != 0 and self.ghost_board[r][c] == -1 :
            if (
              self.owner_board[r][c] == self.owner_board[r + 1][c]
              and self.ghost_board[r + 1][c] == -1 
              and self.owner_board[r][c] == self.owner_board[r + 2][c] 
              and self.ghost_board[r + 2][c] == -1 
              and self.owner_board[r][c] == self.owner_board[r + 3][c] 
              and self.ghost_board[r + 3][c] == -1
            ):
              if (self.owner_board[r][c] == 1):
                winner1 = True
              else:
                winner2 = True
          
    for c in range(cols - 3):
          for r in range(rows - 3):
            if self.owner_board[r][c] != 0 and self.ghost_board[r][c] == -1 :
              if (
                self.owner_board[r][c] == self.owner_board[r + 1][c + 1]
                and self.ghost_board[r + 1][c + 1] == -1 
                and self.owner_board[r][c] == self.owner_board[r + 2][c + 2] 
                and self.ghost_board[r + 2][c + 2] == -1 
                and self.owner_board[r][c] == self.owner_board[r + 3][c + 3] 
                and self.ghost_board[r + 3][c + 3] == -1
              ):
                if (self.owner_board[r][c] == 1):
                  winner1 = True
                else:
                  winner2 = True
    for c in range(3, cols):
          for r in range(rows - 3):
            if self.owner_board[r][c] != 0 and self.ghost_board[r][c] == -1 :
              if (
                self.owner_board[r][c] == self.owner_board[r + 1][c - 1]
                and self.ghost_board[r + 1][c - 1] == -1 
                and self.owner_board[r][c] == self.owner_board[r + 2][c - 2] 
                and self.ghost_board[r + 2][c - 2] == -1 
                and self.owner_board[r][c] == self.owner_board[r + 3][c - 3] 
                and self.ghost_board[r + 3][c - 3] == -1
              ):
                if (self.owner_board[r][c] == 1):
                  winner1 = True
                else:
                  winner2 = True
    self.setWinner(winner1, winner2, draw)


  '''
  Moves:
  0-6: place in columns 0-6 respectively
  7-49:
  row is (move // 7) - 1
  col is mov % 7
  If quantum piece in space, observe it and turn it into a real piece, destroy its linked piece
  and shift everything down
  50-76:
  Place quantum pieces in Columns 
  '''
  def apply(self, move):
    if self.gameOver: return
    #Place Real
    if (move < cols):
      for r in reversed(range(rows)):
        if (self.owner_board[r][move] == 0):
          self.owner_board[r][move] = self.curr_player
          self.curr_player = -1 * self.curr_player
          break
    #Observe Quantum
    elif move < 42 + cols:
      row = move // cols - 1
      col = (move) % cols
      id = self.ghost_board[row][col]
      if id == -1:
        return
      self.ghost_board[row][col] = -1
      breaker = False
      for r in range(rows):
        if breaker:
          break
        for c in range(cols):
          if (self.ghost_board[r][c] == id):
            for k in reversed(range(1, r + 1)):
              self.owner_board[k][c] = self.owner_board[k - 1][c]
              self.ghost_board[k][c] = self.ghost_board[k - 1][c]
            self.owner_board[0][c] = 0
            self.ghost_board[0][c] = -1
            self.curr_player *= -1
            breaker = True
            break
    #Place Quantum
    else:
      first = 0
      move -= 42 + cols
      while move >= cols - first:
        move -= cols - first
        first += 1
      move += first
      for r in reversed(range(rows)):
        if (self.owner_board[r][move] == 0):
          self.owner_board[r][move] = self.curr_player
          self.ghost_board[r][move] = self.id_tracker
          break
      for r in reversed(range(rows)):
        if (self.owner_board[r][first] == 0):
          self.owner_board[r][first] = self.curr_player
          self.ghost_board[r][first] = self.id_tracker
          break
      self.id_tracker += 1
      self.curr_player *= -1
    self.checkGame()


  def legal_moves(self):
    if self.gameOver: return []
    valid_moves = []
    count = 0
    for c in range(cols):
      if self.owner_board[0][c] == 0:
        valid_moves.append(c)
      for r in range(c, cols):
        if c == r and self.owner_board[1][c] == 0:
          valid_moves.append(49 + (count))
        elif self.owner_board[0][c] == 0 and self.owner_board[0][r] == 0 and c != r:
          valid_moves.append(49 + (count))
        count += 1

    for r in range(rows):
      for c in range(cols):
        if self.ghost_board[r][c] != -1:
          valid_moves.append((r * 7 + c) + 7)
    valid_moves.sort()
    return valid_moves
    #for move in valid_moves:
    #  print(move, end = " ")
    

  def print_board(self):
    for r in self.owner_board:
      for c in r:
        print(c, end = " ")
      print()
    print()
    print()
    for r in self.ghost_board:
        for c in r:
          print(c, end = " ")
        print()

  def encode(self):
    p1_real = []
    p2_real = []
    p1_quantum = []
    p2_quantum = []
    quantum_row = []
    quantum_column = []
    for r in range(rows):
      p1_real.append([0] * cols)
      p2_real.append([0] * cols)
      p1_quantum.append([0] * cols)
      p2_quantum.append([0] * cols)
      quantum_column.append([-1] * cols)
      quantum_row.append([-1] * cols)

    rows_dict = {}
    col_dict = {}
    for r in range(rows):
      for c in range(cols):
        if self.owner_board[r][c] == self.curr_player and self.ghost_board[r][c] == -1:
          p1_real[r][c] = 1
        elif self.owner_board[r][c] == -1 * self.curr_player and self.ghost_board[r][c] == -1:
          p2_real[r][c] = 1
        elif self.owner_board[r][c] == self.curr_player:
          p1_quantum[r][c] = 1
        elif self.owner_board[r][c] == -1 * self.curr_player:
          p2_quantum[r][c] = 1
        if self.ghost_board[r][c] != -1:
          if (self.ghost_board[r][c] in rows_dict):
            quantum_row[r][c] = rows_dict.get(self.ghost_board[r][c])/(rows - 1)
            quantum_column[r][c] = col_dict.get(self.ghost_board[r][c])/(cols - 1)
            quantum_row[rows_dict.get(self.ghost_board[r][c])][col_dict.get(self.ghost_board[r][c])] = r/(rows - 1)
            quantum_column[rows_dict.get(self.ghost_board[r][c])][col_dict.get(self.ghost_board[r][c])] = c/(cols - 1)
          else:
            rows_dict[self.ghost_board[r][c]] = r
            col_dict[self.ghost_board[r][c]] = c
    return (p1_real, p2_real, p1_quantum, p2_quantum, quantum_row, quantum_column)

    

        
    

def main():
  game = Game(new = True)
  
  print(game.legal_moves())
  game.apply(55)
  #game.print_board()
  print()
  for matrix in game.encode():
    for r in matrix:
      for c in r:
        print(c, end = " ")
      print()
    print()
  game.apply(6)
  print()
  for matrix in game.encode():
    for r in matrix:
      for c in r:
        print(c, end = " ")
      print()
    print()
  #print()
  #game.apply(62)
  #game.print_board()
  #print()
  #game.apply(42)
  #game.print_board()



if (__name__ == "__main__") :
  main()
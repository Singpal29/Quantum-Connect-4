import random
import qc4.engine as engine
import time
import qc4.MCTS as MCTS
import pandas as pd
import qc4.az_MCTS as az_MCTS
import qc4.model as model
import torch
import config
import qc4.players as players
import qc4.arena as arena


def obviousWin(player):
  game = engine.Game()
  game.owner_board[config.ROWS - 1][config.COLS - 1] = 1
  game.owner_board[config.ROWS - 1][config.COLS - 2] = 1
  game.owner_board[config.ROWS - 1][config.COLS - 3] = 1
  game.apply(player.move(game))
  assert game.winner == 1, "Failed to find winning move"
  print("Winning move found")

def test_invariants(player1, player2):
  arena.play_match(player1, player2, games = 500, swap = True, invariants = True)
  print("Invariants passed")

def main():
  test_invariants(players.RandomPlayer(), players.RandomPlayer())
  obviousWin(players.MCTSPlayer())
  obviousWin(players.NetworkPlayer(players.load_generation(1, 200), 200))
  
  


if __name__ == "__main__":
  main()
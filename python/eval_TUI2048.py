from game_2048 import Board
from model import Model
from config import config as c
import numpy as np
import torch
import time


class Game2048():
  def __init__(self):
    self.board = Board()
    self.model = Model()

    self.model.resnet = torch.load(c.model_latest)

  def eval_step(self):
    board_to_eval = np.zeros([1, 1, c.board_size, c.board_size])
    board_to_eval[0, 0, :, :] = self.board.board / 16

    result = self.model.forward(board_to_eval)[0].tolist()
    print(result)
    result = zip(c.step_label, result)

    for step, score in sorted(result, key=lambda x: x[1], reverse=True):
      if (self.board.if_step(step)):
        print("Step " + step + ".")
        # time.sleep(1)

        return step

  def play(self):
    while self.board.legal_step():
      self.board.draw_board(self.board.score, self.board.get_intutive_board())
      direct = self.eval_step()
      self.board.do_step(direct)
      print("=" * 20)
      print("")
    self.board.draw_board(self.board.score, self.board.get_intutive_board())
    print("GAME OVER!")

if __name__ == "__main__":
  game = Game2048()
  game.play()







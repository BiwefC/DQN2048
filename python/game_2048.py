import numpy as np
import random
import curses
import sys

class Board:
  def __init__(self):
    print("This is from board")
    self.WIDTH = 4
    self.HIGHT = 5
    self.board = np.zeros([self.HIGHT, self.WIDTH], dtype=np.int)
    self.random_generate()
    self.random_generate()

  def random_generate(self):
    free_xy = np.where(self.board == 0)
    free_num = len(free_xy[0])

    index_list = list(range(free_num))
    random.shuffle(index_list)
    index = index_list[0]

    num_list = [1, 1, 1, 2]
    random.shuffle(num_list)
    num = num_list[0]
    self.board[free_xy[0][index], free_xy[1][index]] = num

  def __convert_intutive(self, num):
    if num == 0:
      return ""
    else:
      return 2 ** num

  def get_intutive_board(self):
    board = []
    for i in range(self.HIGHT):
      row = []
      for j in range(self.WIDTH):
        row.append(self.__convert_intutive(self.board[i, j]))
      board.append(row)

    return board

  def draw_board(self, board):
    for row in board:
      row_len = len(row)
      for i in range(row_len):
        print("+" + "-"*7, end="")
      print("+")
      for i in range(row_len):
        print("|{:^7}".format(""), end="")
      print("|")
      for item in row:
        print("|{:^7}".format(item), end="")
      print("|")
      for i in range(row_len):
        print("|{:^7}".format(""), end="")
      print("|")
    for i in range(row_len):
      print("+" + "-"*7, end="")
    print("+")

  def __tight_left(self, board):
    (h, w) = board.shape
    result = np.zeros([h, w], dtype=np.int)
    for i in range(h):
      index = 0
      for j in range(w):
        if board[i, j] != 0:
          result[i, index] = board[i, j]
          index += 1

    return result

  def __merge_left(self, board):
    (h, w) = board.shape
    for i in range(h):
      for j in range(w-1):
        if board[i, j] == board[i, j+1] and board[i, j] != 0:
          board[i, j] = board[i, j] + 1
          board[i, j+1] = 0

    return board

  def step_left(self):
    self.board =  self.__tight_left(self.__merge_left(self.__tight_left(self.board)))

  def step_right(self):
    self.board = np.flip(self.board, axis=1)
    self.step_left()
    self.board = np.flip(self.board, axis=1)

  def step_up(self):
    self.board = self.board.T
    self.step_left()
    self.board = self.board.T

  def step_down(self):
    self.board = self.board.T
    self.step_right()
    self.board = self.board.T

class Game2048(Board):
  def __init__(self):
    print("This is from Game2048")
    Board.__init__(self)


if __name__ == "__main__":
  game = Game2048()
  game.draw_board(game.get_intutive_board())
  while(1):
    direct = input("Input direct: (w/a/s/d)")
    if (direct[0] == "a"):
      game.step_left()
    elif (direct[0] == "d"):
      game.step_right()
    elif (direct[0] == "w"):
      game.step_up()
    elif (direct[0] == "s"):
      game.step_down()

    game.random_generate()
    game.draw_board(game.get_intutive_board())


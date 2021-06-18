import numpy as np
import random
import curses
import sys

class Board:
  def __init__(self):
    print("This is from board")
    self.WIDTH = 4
    self.HIGHT = 4
    self.score = 0
    self.board = np.zeros([self.HIGHT, self.WIDTH], dtype=np.int)
    self.random_generate()
    self.random_generate()

    self.__dir_func = {}
    self.__dir_func["left"] = self.__step_left
    self.__dir_func["right"] = self.__step_right
    self.__dir_func["up"] = self.__step_up
    self.__dir_func["down"] = self.__step_down

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

  def draw_board(self, score, board):
    print("Score: {}".format(score))
    print("")
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
          new_value = board[i, j] + 1
          board[i, j] = new_value
          board[i, j+1] = 0

          self.score += self.__convert_intutive(new_value)

    return board

  def __step_left(self, board):
    return self.__tight_left(self.__merge_left(self.__tight_left(board)))

  def __step_right(self, board):
    return np.flip(self.__step_left(np.flip(board, axis=1)), axis=1)

  def __step_up(self, board):
    return self.__step_left(board.T).T

  def __step_down(self, board):
    return self.__step_right(board.T).T

  def step(self, direct):
    self.board = self.__dir_func[direct](self.board)

  def if_step(self, direct):
    return (self.__dir_func[direct](self.board) != self.board).any()

  def legal_step(self):
    legal_step = []
    for direct in self.__dir_func:
      if self.if_step(direct):
        legal_step.append(direct)

    return legal_step


class Game2048():
  def __init__(self):
    print("This is from Game2048")
    self.board = Board()

  def input_step(self):
    while 1:
      direct = input("Input direct: (w/a/s/d)")
      if len(direct) != 1:
        print("Illegal input!")
      elif (direct[0] == "a"):
        return "left"
      elif (direct[0] == "d"):
        return "right"
      elif (direct[0] == "w"):
        return "up"
      elif (direct[0] == "s"):
        return "down"
      else:
        print("Illegal input!")

  def play(self):
    self.board.draw_board(self.board.score, self.board.get_intutive_board())
    legal_step = self.board.legal_step()
    while legal_step:
      direct = self.input_step()
      if direct in legal_step:
        self.board.step(direct)
        self.board.random_generate()
        self.board.draw_board(self.board.score, self.board.get_intutive_board())
        legal_step = self.board.legal_step()
      else:
        print("Can't step {}".format(direct))
    print("GAME OVER!")


if __name__ == "__main__":
  game = Game2048()
  game.play()



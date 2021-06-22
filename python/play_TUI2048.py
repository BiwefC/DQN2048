from game_2048 import Board


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
      legal_step = self.board.do_step(direct)
      self.board.draw_board(self.board.score, self.board.get_intutive_board())
    print("GAME OVER!")

if __name__ == "__main__":
  game = Game2048()
  game.play()







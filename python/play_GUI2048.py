from flask import Flask, render_template, request
from game_2048 import Board

app = Flask("2048", static_folder="../web/", template_folder="../web/")
board = Board()

@app.route('/')
def root():
  print("Hello World!")
  return render_template("index.html")

@app.route('/newgame', methods=["GET", "POST"])
def newgame():
  print("Start a new game!")
  board.start()
  return {"score": board.score,
          "board": board.get_intutive_board()}

@app.route('/step', methods=["GET", "POST"])
def step():
  direct = request.form.get("direct")
  next_steps = board.do_step(direct)

  return {"end": len(next_steps) == 0,
          "score": board.score,
          "board": board.get_intutive_board()}

app.run(debug=True)


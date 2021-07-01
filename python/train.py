from config import config as c
from game_2048 import Board
from model import Model
import numpy as np

os.makedir(c.weights_dir, exist_ok=True)

main_board = Board()
target_model = Model()
eval_model = Model()

if os.path.exists(c.model_latest):
    eval_model.load(c.model_latest)

if os.path.exists(c.model_target):
    target_model.load(c.model_target)

for i in range(c.target_update_num):
    state_batch = []
    qeval_batch = []
    for j in range(c.train_step_num):
        state_batch.append(self.board)
        if main_board.legal_step:
            reward = np.zeros(4, 4)
            board_to_eval = np.zeros(4, 1, c.board_size, c.board_size)
            for (index, step) in enumerate(c.step_label):
                if main_board.if_step(step):
                    next_board = Board(main_board)
                    next_board.step(step)
                    reward = next_board.score - main_board.score
                    board_to_eval[index, 1, :, :] = next_board.board
                else:
                    reward = -5.0
                    board_to_eval[index, 1, :, :] = main_board.board
            q_next_max = np.amax(target_model.forward(board_to_eval), axis=1)
            q_target = reward + c.q_value_gamma*q_next_max

            index = int(np.where(q_target == q_target.max())[1][0])
            main_board.step(c.step_label[index])

        else:
            q_target = np.zeros(4, 4)
            q_target[:,:] = -31.

            main_board.start()

        qeval_batch.append(q_target)

        state_batch = np.array(state_batch)
        qeval_batch = np.array(qeval_batch)

    eval_model.train(state_batch, qeval_batch)

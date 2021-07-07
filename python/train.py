from config import config as c
from game_2048 import Board
from model import Model
import numpy as np
import os
import torch
import time
import math

os.makedirs(c.weights_dir, exist_ok=True)

main_board = Board()
target_model = Model()
eval_model = Model()

if os.path.exists(c.model_latest):
    eval_model.resnet = torch.load(c.model_latest)

if os.path.exists(c.model_target):
    target_model.resnet = torch.load(c.model_target)

def evaluate_once(board):
    if board.legal_step():
        reward = np.zeros([4*c.eval_repeat,])
        board_to_eval = np.zeros([4*c.eval_repeat, 1, c.board_size, c.board_size])
        for i in range(c.eval_repeat):
            for (index, step) in enumerate(c.step_label):
                if board.if_step(step):
                    next_board = Board(board)
                    next_board.do_step_no_check(step)
                    reward[i*4+index] = math.log(next_board.score - board.score + 1, 2) * 2 / 16
                    board_to_eval[i*4+index, 0, :, :] = next_board.board / 16
                else:
                    reward[i*4+index] = -5.0 / 16
                    board_to_eval[i*4+index, 0, :, :] = board.board / 16
        q_next_max = np.amax(target_model.forward(board_to_eval), axis=1)
        q_target = reward + c.q_value_gamma*q_next_max

        index = int(np.where(q_target == q_target.max())[0][0]) % 4
        # print(board.board)
        # print(q_target)
        # print(c.step_label[index])

        # assert (board.if_step(c.step_label[index]))
        board.do_step_no_check(c.step_label[index])
        # print(board.board)
        # print(board.legal_step())
        # print("+"*20)

    else:
        q_target = np.zeros([4*c.eval_repeat,])
        q_target[:] = -15. / 16

        board.start()
        # print("start new game")

    q_target = q_target.reshape([c.eval_repeat, 4])

    return q_target

while True:
    for i in range(c.target_update_num):
        state_batch = []
        qeval_batch = []
        for j in range(c.batch_size * c.batch_num):
            for k in range(c.eval_repeat):
                state_batch.append([main_board.board])
            q_target = evaluate_once(main_board)

            qeval_batch.extend(q_target.tolist())

        state_batch = np.array(state_batch)
        qeval_batch = np.array(qeval_batch)

        # print(state_batch)
        # print(qeval_batch)

        # print(state_batch.shape)
        # print(qeval_batch.shape)

        # assert(0)

        eval_model.train(state_batch, qeval_batch)
        model_name = time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime()) + ".pkl"
        model_path = c.weights_dir + "/" + model_name

        torch.save(eval_model.resnet, model_path)

        os.system("rm {}".format(c.model_latest))
        os.system("ln -s {} {}".format(model_path, c.model_latest))

    os.system("rm {}".format(c.model_target))
    os.system("ln -s {} {}".format(model_path, c.model_target))
    target_model.resnet = torch.load(c.model_latest)
    print("Load new target model.")


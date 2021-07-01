class Config(object):
    def __init__(self):
        # board
        self.board_size = 4
        self.step_num = 4
        self.step_label = ["left", "right", "up", "down"]

        # weight
        self.weights_dir = "../weights"
        self.model_latest = self.weights_dir + "/latest.pkl"
        self.model_target = self.weights_dir + "/target.pkl"

        # hyper
        self.filters = 32
        self.value_hidden_units = 128
        self.value_loss_factor = 1.0
        self.batchnorm_momentum = 0.1

        # train
        self.target_update_num = 10
        self.recent_count = 10000
        self.batch_size = 256
        self.learning_rate = 1e-4
        self.train_count = 2
        self.train_epoch = 1

        # selfplay
        self.selfplay_process_count = 3
        self.selfplay_target_rounds = 500

        # evaluate
        self.eval_process_count = 3
        self.eval_target_rounds = 50

config = Config()

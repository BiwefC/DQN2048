import torch
from torch.autograd import Variable
import resnet
from config import config as c

class Model:
    def __init__(self, is_train=True):
        self.eval_net = resnet.Resnet()
        self.eval_net.cuda()

        if is_train:
            self.optimizer = torch.optim.SGD(
                self.resnet.parameters(),
                lr=c.learning_rate,
                momentum=0.9,
                weight_decay=1E-4)

            self.policy_loss_fn = torch.nn.MSELoss()

    def forward(self, observation):
        count = np.size(observation, 0)

        with torch.no_grad():
            observation = Variable(torch.from_numpy(observation).float().cuda())

        self.eval_net.eval()
        p = self.eval_net.forward(observation)

        p = np.reshape(p, [count, c.step_num])

        return p

    def train(self, observation, q_target):
        n_samples = np.size(observation, 0)
        n_batches = int(n_samples / c.batch_size)

        train_policy_loss = 0.0

        self.eval_net.train()

        for i in range(n_batches):
            if (i + 1) % 100 == 0:
                print("Training batch {} of {}...".format(i+1, n_batches))

            start, end = i * c.batch_size, (i+1) * c.batch_size
            obsv_var = Variable(torch.from_numpy(observation[start:end]).float().cuda())
            qtar_var = Variable(torch.from_numpy(q_target[start:end]).float().cuda())

            self.optimizer.zero_grad()
            q_eval = self.eval_net.forward(obsv_var)

            policy_loss = self.policy_loss_fn.forward(q_eval, qtar_var)

            train_policy_loss += policy_loss.data.item()

            policy_loss.backward()

            self.optimizer.step()


        print("Train policy_loss = {}".format(train_policy_loss / n_batches))

        with open(c.weight_dir + '/log/train.log', 'a') as f:
            f.write("Train policy_loss = {}\n".format(train_policy_loss / n_batches))


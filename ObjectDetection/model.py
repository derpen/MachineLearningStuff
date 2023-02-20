from torch import nn

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.order = nn.Sequential(
            nn.Conv2d(3, 16, (3, 3)),
            nn.MaxPool2d((3,3)),

            nn.Conv2d(16, 32, (3,3)),
            nn.MaxPool2d((3,3)),

            nn.Conv2d(32, 16, (3,3)),
            nn.MaxPool2d((3,3)),

            nn.Flatten(),
            nn.Linear(5632, 64),
            nn.ReLU(),
            nn.Linear(64, 5)
        ) 

    def forward(self, x):
        x = self.order(x)
        return x
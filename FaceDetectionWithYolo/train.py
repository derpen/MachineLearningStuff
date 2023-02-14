import torch
import torch.optim as optim
import torchvision.transforms as transforms
from tqdm import tqdm
from torch import nn
from model import Network
from dataset import GetData
from torch.utils.data import DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = Network().to(device)

# uncomment this one to continue training
model.load_state_dict(torch.load('SelfMade.pt'))

batch_size = 8
root_dir = 'datasets/Face'
transforms = transforms.Compose([
    transforms.ToTensor()
])
dataset = GetData(root_dir, transform=transforms)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

learning_rate = 1e-3
num_epochs = 500
# criterion = nn.CrossEntropyLoss()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

for epochs in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(tqdm(data_loader)):
        x, y = data
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()

        yhat = model(x)
        loss = criterion(yhat, y)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print('Epoch [%d], Loss: %.9f' % (epochs+1, running_loss / len(data_loader)))

modelname = "SelfMade.pt"
torch.save(model.state_dict(), modelname)
print('Finished Training, model saved as ' + modelname)
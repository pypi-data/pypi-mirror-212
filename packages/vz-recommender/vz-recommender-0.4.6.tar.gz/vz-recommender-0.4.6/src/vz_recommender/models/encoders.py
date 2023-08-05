from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
import torch


class VariationalEncoder(nn.Module):
    def __init__(self, latent_dims, input_dim):
        super().__init__()
        self.linear1 = nn.Linear(input_dim, input_dim//2)
        self.linear2 = nn.Linear(input_dim//2, latent_dims)
        self.linear3 = nn.Linear(input_dim//2, latent_dims)
        self.input_dim = input_dim

        self.N = torch.distributions.Normal(0, 1)
        self.kl = 0

    def forward(self, x):
        x = F.relu(self.linear1(x))
        mu =  self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        z = mu + sigma*self.N.sample(mu.shape).to(x.device)
        self.kl = (sigma**2 + mu**2 - torch.log(sigma) - 1/2).sum()
        return z#, self.kl

class Decoder(nn.Module):
    def __init__(self, latent_dims, input_dim):
        super().__init__()
        self.linear1 = nn.Linear(latent_dims, input_dim//2)
        self.linear2 = nn.Linear(input_dim//2, input_dim)
        self.latent_dims = latent_dims

    def forward(self, z):
        z = F.relu(self.linear1(z))
        z = torch.sigmoid(self.linear2(z))
        return z

class LinearVAE(nn.Module):
    def __init__(self, latent_dims, input_dim):
        super().__init__()
        self.encoder = VariationalEncoder(latent_dims=latent_dims, input_dim=input_dim)
        self.decoder = Decoder(latent_dims=latent_dims, input_dim=input_dim)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)#, kl



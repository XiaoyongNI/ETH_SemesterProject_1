import torch
import math

#########################
### Design Parameters ###
#########################
m = 4
n = 4

m1x_0 = torch.zeros(m, 1)
m2x_0 = torch.tensor([[0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      [0,0,0,0]]).float()

# Time step span
delta_t = 1

##########################################
### Dynamics For No Air Friction Movement ###
##########################################
# Taylor approximation
F_dim = torch.tensor([[1.0, delta_t],
                      [0,1.0]])


# Model Transformations
F_design = torch.block_diag(F_dim, F_dim)

H_design = torch.eye(n) 
'''
H_design = torch.tensor([[0,1.,0,0],
                          [0,0,0,1.]])
'''
# Noise Parameters
sigma_q = 0.7
sigma_r = 0.1

# Noise matrix per dimension
Q_dim = torch.diagflat(torch.tensor([delta_t, delta_t]))

# Noise Matrices
Q = (sigma_q**2) * torch.block_diag(Q_dim, Q_dim)


R = torch.tensor([[700,0,0,0],
                  [0,0.01,0,0],
                  [0,0,700,0],
                  [0,0,0,0.01]]).float()
'''
R = torch.eye(n) * (sigma_r**2)
'''
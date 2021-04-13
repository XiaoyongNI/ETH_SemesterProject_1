import torch
import math

#########################
### Design Parameters ###
#########################
m = 2
n = 2

m1x_0 = torch.ones(m, 1) * 0.1
m2x_0 = torch.zeros(m,m)

T = 10

#######################
### True Parameters ###
#######################
alpha_mot = 0.9
beta_mot = 1.1
phi_mot = math.pi/10
a_mot = 1
beta_obs = 1
a_obs = 0

# Noise Parameters
sigma_q = 0.1
sigma_r = 0.1

# Noise Matrices
Q = (sigma_q**2) * torch.eye(m)
R = (sigma_r**2) * torch.eye(m)

########################
### Model Parameters ###
########################
alpha_mot_mod = 1
beta_mot_mod_ = 1
phi_mot_mod = 0
a_mot_mod = 1
beta_obs_mod = 1
a_obs_mod = 0

# Noise Parameters
sigma_q = 0.7
sigma_r = 0.1

# Noise Matrices
Q = (sigma_q**2) * torch.eye(m)
R = (sigma_r**2) * torch.eye(m)
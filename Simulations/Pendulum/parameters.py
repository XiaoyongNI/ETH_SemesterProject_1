import torch
import math

if torch.cuda.is_available():
    cuda0 = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc.
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
else:
   cuda0 = torch.device("cpu")
   print("Running on the CPU")

#########################
### Design Parameters ###
#########################
m = 2
n = 2

m1x_0 = torch.ones(m, 1) 
m1x_0_design_test = torch.ones(m, 1)
m2x_0 = 0 * 0 * torch.eye(m)

# Decimation ratio
ratio = 1

# Length of Time Series Sequence
T = math.ceil(30 / ratio)
T_test = math.ceil(30 / ratio)

##########################################
### Generative Parameters For Pendulum ###
##########################################

delta_t_gen =  1e-5
delta_t = delta_t_gen/ratio

H_design = torch.eye(m)

H_design_inv = torch.inverse(H_design)

# Noise Parameters
r_dB = 0
lambda_r = math.sqrt(10**(-r_dB/10))
nx = 0
lambda_q = lambda_r * nx

# Noise Matrices
Q_non_diag = False
R_non_diag = False

Q = (lambda_q**2) * torch.eye(m)

if(Q_non_diag):
    q_d = lambda_q**2
    q_nd = (lambda_q **2)/2
    Q = torch.tensor([[q_d, q_nd, q_nd],[q_nd, q_d, q_nd],[q_nd, q_nd, q_d]])

R = (lambda_r**2) * torch.eye(n)

if(R_non_diag):
    r_d = lambda_r**2
    r_nd = (lambda_r **2)/2
    R = torch.tensor([[r_d, r_nd, r_nd],[r_nd, r_d, r_nd],[r_nd, r_nd, r_d]])

#########################
### Model Parameters ####
#########################

m1x_0_mod = m1x_0
m1x_0_mod_test = m1x_0_design_test
m2x_0_mod = 0 * 0 * torch.eye(m)

# Sampling time step
delta_t_mod = delta_t

# Length of Time Series Sequence
T_mod = math.ceil(T * ratio)
T_test_mod = math.ceil(T_test * ratio)

#######################################
#### Model Parameters For Pendulum ####
#######################################

H_mod = torch.eye(n)
#H_mod = H_design
H_mod_inv = torch.inverse(H_mod)

# Noise Parameters
lambda_q_mod = 0.1
lambda_r_mod = 0.1

# Noise Matrices
Q_mod = (lambda_q_mod**2) * torch.eye(m)
R_mod = (lambda_r_mod**2) * torch.eye(n)
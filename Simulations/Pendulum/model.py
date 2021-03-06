import math
import torch
torch.pi = torch.acos(torch.zeros(1)).item() * 2 # which is 3.1415927410125732
from torch import autograd
from parameters import m, n, delta_t, delta_t_gen, H_design, delta_t_mod

if torch.cuda.is_available():
    cuda0 = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc.
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
else:
   cuda0 = torch.device("cpu")
   print("Running on the CPU")

# def f_gen(x):

#     #A = torch.add(torch.einsum('nhw,wa->nh', B, x).T,C)
#     A = torch.add(torch.reshape(torch.matmul(B, x),(m,m)).T,C)
    
#     # Taylor Expansion for F    
#     F = torch.eye(m)
#     for j in range(1,J+1):
#         F_add = (torch.matrix_power(A*delta_t_gen, j)/math.factorial(j)).to(cuda0)
#         F = torch.add(F, F_add).to(cuda0)

#     return torch.matmul(F, x)

def f(x):
    g = 1 # Gravitational Acceleration
    L = 10 # Radius of pendulum
    damping =  - 0.5*x[1]
    result = [x[1]*delta_t, (-g/L * torch.sin(x[0])  + damping)*delta_t]
    result = torch.squeeze(torch.tensor(result))
    # print(result.size())
    return result

def h(x):
    return torch.matmul(H_design,x).to(cuda0)
    #return toSpherical(x)

# def fInacc(x):

#     #A = torch.add(torch.einsum('nhw,wa->nh', B, x).T,C)
#     A = torch.add(torch.reshape(torch.matmul(B_mod, x),(m,m)).T,C_mod)
    
#     # Taylor Expansion for F    
#     F = torch.eye(m)
#     for j in range(1,J_mod+1):
#         F_add = (torch.matrix_power(A*delta_t_mod, j)/math.factorial(j)).to(cuda0)
#         F = torch.add(F, F_add).to(cuda0)

#     return torch.matmul(F, x)

# def hInacc(x):
#     return torch.matmul(H_mod,x)
#     #return toSpherical(x)

def getJacobian(x, a):
    
    # if(x.size()[1] == 1):
    #     y = torch.reshape((x.T),[x.size()[0]])
    try:
        if(x.size()[1] == 1):
            y = torch.reshape((x.T),[x.size()[0]])
    except:
        y = torch.reshape((x.T),[x.size()[0]])
        
    if(a == 'ObsAcc'):
        g = h
    elif(a == 'ModAcc'):
        g = f
    elif(a == 'ObsInacc'):
        g = hInacc
    elif(a == 'ModInacc'):
        g = fInacc

    Jac = autograd.functional.jacobian(g, y)
    Jac = Jac.view(-1,m)
    return Jac



# def hInv(y):
#     return torch.matmul(H_design_inv,y)
#     #return toCartesian(y)


# def hInaccInv(y):
#     return torch.matmul(H_mod_inv,y)
#     #return toCartesian(y)

'''
x = torch.tensor([[1],[1],[1]]).float() 
H = getJacobian(x, 'ObsAcc')
print(H)
print(h(x))

F = getJacobian(x, 'ModAcc')
print(F)
print(f(x))
'''
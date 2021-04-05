import torch
torch.pi = torch.acos(torch.zeros(1)).item() * 2 # which is 3.1415927410125732

from KalmanNet_sysmdl import SystemModel
from KalmanNet_data import DataGen, DataLoader_GPU
from KalmanNet_data import F, H, T, T_test, m1_0, m2_0

from KalmanFilter_test import KFTest
from RTS_Smoother_test import S_Test
from KalmanNet_data import N_E, N_CV, N_T

from Pipeline_RTS import Pipeline_RTS as Pipeline
from RTSNet_nn import RTSNetNN
from datetime import datetime

from DataAnalysis import DataAnalysis
from Plot import Plot_RTS as Plot

if torch.cuda.is_available():
   device = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc.
   torch.set_default_tensor_type('torch.cuda.FloatTensor')
   print("Running on the GPU")
else:
   device = torch.device("cpu")
   print("Running on the CPU")

   

print("Pipeline Start")

################
### Get Time ###
################
today = datetime.today()
now = datetime.now()
strToday = today.strftime("%m.%d.%y")
strNow = now.strftime("%H:%M:%S")
strTime = strToday + "_" + strNow
print("Current Time =", strTime)


####################
### Design Model ###
####################
r = 1
q = 1

SysModel_design = SystemModel(F, q, H, r, T, T_test)
SysModel_design.InitSequence(m1_0, m2_0)

# Inaccurate model knowledge based on matrix rotation
alpha_degree = 10
rotate_alpha = torch.tensor([alpha_degree/180*torch.pi]) 
cos_alpha = torch.cos(rotate_alpha)
sin_alpha = torch.sin(rotate_alpha)
rotate_matrix = torch.tensor([[cos_alpha, -sin_alpha],
                              [sin_alpha, cos_alpha]])
# print(rotate_matrix)
F_rotated = torch.mm(F,rotate_matrix) #inaccurate process model
# H_rotated = torch.mm(H,rotate_matrix) #inaccurate observation model
SysModel_rotate = SystemModel(F_rotated, q, H, r, T, T_test)
SysModel_rotate.InitSequence(m1_0, m2_0)


###################################
### Data Loader (Generate Data) ###
###################################
# print("Start Gen Data")
dataFolderName = 'Data' + '/'
# dataFileName = 'data_rotateF10_2x2_r1q1_T20_Ttest20.pt'
# DataGen(SysModel_rotate, dataFolderName + dataFileName, T, T_test)
# print("Data Load")
# [train_input, train_target, cv_input, cv_target, test_input, test_target] = DataLoader_GPU(dataFolderName + dataFileName)


##############################
### Evaluate Kalman Filter ###
##############################
# print("Evaluate Kalman Filter")
# [MSE_KF_linear_arr, MSE_KF_linear_avg, MSE_KF_dB_avg] = KFTest(SysModel_design, test_input, test_target)

##############################
### Evaluate RTS Smoother ###
##############################
# print("Evaluate RTS Smoother")
# [MSE_RTS_linear_arr, MSE_RTS_linear_avg, MSE_RTS_dB_avg] = S_Test(SysModel_design, test_input, test_target)

##############################
###  Compare KF and RTS    ###
##############################
# r = torch.tensor([2, 1, 0.5, 0.1])
# r = torch.sqrt(r)
# q = r
# MSE_KF_RTS_dB = torch.empty(size=[2,len(r)])
# dataFileName = ['data_2x2_r2q2_T20_Ttest20.pt','data_2x2_r1q1_T20_Ttest20.pt','data_2x2_r0.5q0.5_T20_Ttest20.pt','data_2x2_r0.1q0.1_T20_Ttest20.pt']
# for rindex in range(0, len(r)):
#     #Generate and load data
#     SysModel_design = SystemModel(F, torch.squeeze(q[rindex]), H, torch.squeeze(r[rindex]), T, T_test)  
#     SysModel_design.InitSequence(m1_0, m2_0)
#     DataGen(SysModel_design, dataFolderName + dataFileName[rindex], T, T_test)
#     [train_input, train_target, cv_input, cv_target, test_input, test_target] = DataLoader_GPU(dataFolderName + dataFileName[rindex])
#     #Evaluate KF and RTS
#     [MSE_KF_linear_arr, MSE_KF_linear_avg, MSE_KF_dB_avg] = KFTest(SysModel_design, test_input, test_target)
#     [MSE_RTS_linear_arr, MSE_RTS_linear_avg, MSE_RTS_dB_avg] = S_Test(SysModel_design, test_input, test_target)
#     MSE_KF_RTS_dB[0,rindex] = MSE_KF_dB_avg
#     MSE_KF_RTS_dB[1,rindex] = MSE_RTS_dB_avg

# PlotfolderName = 'Graphs' + '/'
# modelName = 'Linear_KFandRTS'  
# Plot = Plot(PlotfolderName, modelName)
# print("Plot")
# Plot.KF_RTS_Plot(r, MSE_KF_RTS_dB)



#######################
### RTSNet Pipeline ###
#######################

# RTSNet_Pipeline = Pipeline(strTime, "RTSNet", "RTSNet")
# RTSNet_Pipeline.setssModel(SysModel_design)
# RTSNet_model = RTSNetNN()
# RTSNet_model.Build(SysModel_design)
# RTSNet_Pipeline.setModel(RTSNet_model)
# RTSNet_Pipeline.setTrainingParams(n_Epochs=200, n_Batch=30, learningRate=1E-3, weightDecay=5E-5)
# RTSNet_Pipeline.NNTrain(N_E, train_input, train_target, N_CV, cv_input, cv_target)
# RTSNet_Pipeline.NNTest(N_T, test_input, test_target)
# RTSNet_Pipeline.PlotTrain_RTS(MSE_KF_linear_arr, MSE_KF_dB_avg, MSE_RTS_linear_arr, MSE_RTS_dB_avg)
# RTSNet_Pipeline.save()

# matlab_import = DataAnalysis()
# matlab_import.main(MSE_RTS_dB_avg)


#######################################
### Compare RTSNet and RTS Smoother ###
#######################################
r = torch.tensor([4, 2, 1, 0.5, 0.1])
r = torch.sqrt(r)
q = r
MSE_RTS_dB = torch.empty(size=[3,len(r)])
dataFileName = ['data_2x2_r4q4_T20_Ttest20.pt','data_2x2_r2q2_T20_Ttest20.pt','data_2x2_r1q1_T20_Ttest20.pt','data_2x2_r0.5q0.5_T20_Ttest20.pt','data_2x2_r0.1q0.1_T20_Ttest20.pt']
for rindex in range(0, len(r)):
    #Generate data
    # SysModel_design = SystemModel(F, torch.squeeze(q[rindex]), H, torch.squeeze(r[rindex]), T, T_test)  
    # SysModel_design.InitSequence(m1_0, m2_0)
    # DataGen(SysModel_design, dataFolderName + dataFileName[rindex], T, T_test)
    #Load data
    [train_input, train_target, cv_input, cv_target, test_input, test_target] = DataLoader_GPU(dataFolderName + dataFileName[rindex])
    #Evaluate RTS Smoother with perfect SS knowledge
    [MSE_RTS_linear_arr, MSE_RTS_linear_avg, MSE_RTS_dB[0,rindex]] = S_Test(SysModel_design, test_input, test_target)
    #Evaluate RTS Smoother with inaccurate SS knowledge
    [MSE_RTS_linear_arr, MSE_RTS_linear_avg, MSE_RTS_dB[1,rindex]] = S_Test(SysModel_rotate, test_input, test_target)
    #Evaluate RTSNet with inaccurate SS knowledge
    RTSNet_Pipeline = Pipeline(strTime, "RTSNet", "RTSNet")
    RTSNet_Pipeline.setssModel(SysModel_rotate)
    RTSNet_model = RTSNetNN()
    RTSNet_model.Build(SysModel_rotate)
    RTSNet_Pipeline.setModel(RTSNet_model)
    RTSNet_Pipeline.setTrainingParams(n_Epochs=1000, n_Batch=50, learningRate=1E-3, weightDecay=5E-4)
    RTSNet_Pipeline.NNTrain(N_E, train_input, train_target, N_CV, cv_input, cv_target)
    RTSNet_Pipeline.NNTest(N_T, test_input, test_target)
    MSE_RTS_dB[2,rindex] = RTSNet_Pipeline.MSE_test_dB_avg

PlotfolderName = 'Graphs' + '/'
modelName = 'Linear_RTSandRTSNet'  
Plot = Plot(PlotfolderName, modelName)
print("Plot")
Plot.rotate_RTS_Plot(r, MSE_RTS_dB)



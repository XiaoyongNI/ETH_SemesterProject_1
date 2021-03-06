import torch

class SystemModel:

    def __init__(self, F, q, H, r, T, T_test):

        ####################
        ### Motion Model ###
        ####################
        self.F = F
        self.m = self.F.size()[0]

        self.q = q
        self.Q = q * q * torch.eye(self.m)

        #########################
        ### Observation Model ###
        #########################
        self.H = H
        self.n = self.H.size()[0]

        self.r = r
        self.R = r * r * torch.eye(self.n)

        #Assign T and T_test
        self.T = T
        self.T_test = T_test

    #####################
    ### Init Sequence ###
    #####################
    def InitSequence(self, m1x_0, m2x_0):

        self.m1x_0 = m1x_0
        self.m2x_0 = m2x_0


    #########################
    ### Update Covariance ###
    #########################
    def UpdateCovariance_Gain(self, q, r):

        self.q = q
        self.Q = q * q * torch.eye(self.m)

        self.r = r
        self.R = r * r * torch.eye(self.n)

    def UpdateCovariance_Matrix(self, Q, R):

        self.Q = Q

        self.R = R


    #########################
    ### Generate Sequence ###
    #########################
    def GenerateSequence(self, Q_gen, R_gen, T):
        # Pre allocate an array for current state
        self.x = torch.empty(size=[self.m, T])
        # Pre allocate an array for current observation
        self.y = torch.empty(size=[self.n, T])
        # Set x0 to be x previous
        self.x_prev = self.m1x_0

        # Generate Sequence Iteratively
        for t in range(0, T):
            ########################
            #### State Evolution ###
            ########################
            xt = self.F.matmul(self.x_prev)

            # Process Noise
            mean = torch.zeros([self.m,1])
            eq = torch.normal(mean, self.q)
            # eq = np.random.multivariate_normal(mean, Q_gen, 1)
            # eq = torch.transpose(torch.tensor(eq), 0, 1)
            # eq = eq.type(torch.float)

            # Additive Process Noise
            xt = torch.add(xt,eq)

            ################
            ### Emission ###
            ################
            yt = self.H.matmul(xt)

            # Observation Noise
            mean = torch.zeros([self.n,1])
            er = torch.normal(mean, self.r)
            # mean = torch.zeros(self.n)
            # er = np.random.multivariate_normal(mean, R_gen, 1)
            # er = torch.transpose(torch.tensor(er), 0, 1)

            # Additive Observation Noise
            yt = torch.add(yt,er)

            ########################
            ### Squeeze to Array ###
            ########################

            # Save Current State to Trajectory Array
            self.x[:, t] = torch.squeeze(xt)

            # Save Current Observation to Trajectory Array
            self.y[:, t] = torch.squeeze(yt)

            ################################
            ### Save Current to Previous ###
            ################################
            self.x_prev = xt

    ######################
    ### Generate Batch ###
    ######################
    def GenerateBatch(self, size, T):

        # Allocate Empty Array for Input
        self.Input = torch.empty(size, self.n, T)

        # Allocate Empty Array for Target
        self.Target = torch.empty(size, self.m, T)

        ### Generate Examples
        for i in range(0, size):
            # Generate Sequence

            self.GenerateSequence(self.Q, self.R, T)

            # Training sequence input
            self.Input[i, :, :] = self.y

            # Training sequence output
            self.Target[i, :, :] = self.x


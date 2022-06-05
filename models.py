import numpy as np
from scipy import stats

class OLS:
    
    def __init__(self):
        self.X = []
        self.Y = []
        self.beta = []
        self.residuals = []
        self.yhat = []
        self.rss = 0
        self.tss = 0
        self.r2 = 0
        self.adj_r2 = 0
        self.mse = 0
        self.se = []
        self.t = []
        self.p = []
        self.dw = 0
        self.intercept = ''

    def fit(self, X, Y, intercept=True):
        Ymean = Y.mean()
        if intercept == True:
            X_matrix = np.insert(X, 0, 1, axis=1)
            self.intercept=True
        else:
            self.intercept = False
            X_matrix = X
        col = X.shape[1]
        row = X.shape[0]
        self.X = X_matrix
        self.beta = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X_matrix), X_matrix)), np.transpose(X_matrix)), Y)
        self.yhat = np.dot(X_matrix,self.beta) 
        self.Y = Y
        self.residuals = self.Y  - self.yhat  
        self.tss = sum([(i-Ymean)**2 for i in self.Y])
        self.rss = sum([i**2 for i in self.residuals])
        self.r2 = 1 - (self.rss/self.tss)
        self.adj_r2 = 1 - (((1-self.r2) * (row - 1)) / (row - col - 1)) 
        self.mse = self.rss / row
        self.se = np.sqrt(np.diagonal(np.dot(np.dot(np.transpose(self.residuals), self.residuals) / (row - col), np.linalg.inv(np.dot(np.transpose(X_matrix), X_matrix)))))
        for i in range(len(self.beta)):
            self.t.append(self.beta[i]/self.se[i])
        self.p = [2*(1-stats.t.cdf(np.abs(i),(row-col))) for i in self.t]
        esum = sum([(self.residuals[i] - self.residuals[i-1])**2 for i in range(row) if i != 0])
        self.dw = esum/self.rss
        return self.beta

    def test(self, X, Y):
        Ymean = Y.mean()
        if self.intercept == True:
            X_matrix = np.insert(X, 0, 1, axis=1)
        else:
            X_matrix = X
        col = X.shape[1]
        row = X.shape[0]
        pred = np.dot(X_matrix, self.beta)
        residuals = Y - pred
        tss = sum([(i-Ymean)**2 for i in Y])
        rss = sum([i**2 for i in residuals])
        r2 = 1 - (rss/tss)
        adj_r2 = 1 - (((1-r2) * (row - 1)) / (row - col - 1)) 
        mse = rss / row        
        esum = sum([(residuals[i] - residuals[i-1])**2 for i in range(row) if i != 0])
        dw = esum/rss
        return residuals, r2, adj_r2, mse, dw, pred



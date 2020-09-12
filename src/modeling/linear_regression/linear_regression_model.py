# Importing third party libraries
from sklearn.metrics import mean_squared_error
import numpy as np


class LinerRegression:
    """
    Class implementing muplitple linear regression.
    For finding minimum of a cost/score function and updating coefficients it uses batch gradient descent.
    """
    
    def __init__(self, alpha=0.01, num_iter=300):
        """
        Initializes parameters for model.
        
        Params:
        alpha -> learning rate.
        num_iter -> number of iterations
        """
        self.alpha = alpha
        self.num_iter = num_iter
        self.mse = []

    def fit(self, x, y):        
        """
        Fits the model based on provided training data.
        
        Params:
        x -> training set observations.
        y -> training set output variable.
        """
        # Training data 
        self.x = x
        self.y = y 
        self.input_shape = x[0].shape
        
        # Weights - coefficients for linear regression
        # (W1*X1 + W2*X2 + ... + Wn*Xn + W0)
        rows, columns = x.shape
        self.w = np.zeros(columns + 1) 
                
        # Number of training data points
        # (for calculating cost function)
        self.m = rows 
        
        # Train the model
        self._train()
        
    
    def predict(self, x):
        """
        Based on the current parameters (weights) in the liner regression model, calculates prediction,
        bases on the hypothesis: h(x) = wo + w1*x1 + ... + wn*xn
        Shape of provided observation/observations, from which the prediction is to be made must be the same,
        as the shape of the training data used to fit this model
        
        Params:
        x -> numpy 1d array as a single observation or 2d array for prdicting outcome on multiple observations. 
        Observations must have the same number of features as the train data for fitting this model. 
        """
        predictions = []
        if x.shape == self.input_shape:
            # Input x is one observation
            y = self._calculate_hypothesis(x)
            predictions.append(y)
           
        else:
            # Input x is matrix, array of observations
            for observation in x:
                if observation.shape != self.input_shape:
                    raise Exception(f'Input shape for model is ({self.input_shape}), but {x.shape} was provided')
                y = self._calculate_hypothesis(observation)
                predictions.append(y)
        return predictions   
        
    
    def shape(self):
        """Returns the expected shape of input observations (required number of features)."""
        return self.input_shape
    
    def _calculate_hypothesis(self, x):
        """
        Calculates multiple linear regression hyposthesis based on the current weights in regression class.
        Hypothesis: W1*X1 + W2*X2 + ... + Wn*Xn + W0
        """
        # W0 is the last element in weights array
        y = self.w[-1] 
        for i in range(len(x)):
            y+= x[i] * self.w[i]
        return y
    
    def _train(self):
        """
        Training the multiple linear regression model, by adjusting coefficients/weights.
        It goes through selected numbed of iterations to update the weights.
        """
        for i in range(self.num_iter):
            y_pred = self.predict(self.x)
            self._update_weights(y_pred)
            mse = mean_squared_error(self.y, y_pred)
            self.mse.append(mse)
            print(f'Iteration {i}, error: {mse}')
            
    def _update_weights(self, y_pred):
        gradient = self._partial_derrivatives(y_pred) 
        self.w = self.w - self.alpha * gradient
        
    def _partial_derrivatives(self, y_pred):
        """
        Calculating partial derivatives for each weight:
        d(J(w))/dw0 = 1/m * Sum(y_pred - y)
        d(J(w))/dwi = 1/m * Sum(y_pred - y)*Xi
        """ 
        gradient = np.zeros(len(self.w))
        for i in range(len(self.w)):
            for j in range(self.m):
                if i == len(self.w) - 1:
                    # Last weight in weight vector is w0
                    # Different formula for partial derivative for w0
                    gradient[i] = gradient[i] - (self.y[j] - y_pred[j])
                else:
                    # Different formula for every other weight
                    gradient[i] = gradient[i] - (self.y[j] - y_pred[j]) * self.x[j][i] 
        return gradient/self.m
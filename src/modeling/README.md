# Real estate models

In this section we're exploring real estate data only for flats that for sale and are located in Belgrade. After data exploration, the cleaned dataset is exported to be used for training of our models.

As a benchmark, baseline models - the skitlearn models are trained and evaluated. We're implementing equivalent custom models from scratch for:
- Linear regression
- SVM kernel classification

Our custom models are being exported and later used in the application to predict and classify the real estate price.


# Project structure

All of the models, our custom ones and the sklearn ones are trained in jupyter notebooks.

Under this project you will find three directories:
- `eda` - containing notebook where data is analysed and prepared for the training.
- `linear_regression` - containes netebooks for evaluating sklearn regression model as a baseline and notebook for training our custom model implementation.
- `classification` - containes notebooks for evaluating various sklearn kernel SVM models as a baseline and notebook for training our custom model implementation.

Before models are trained, there is a selection of a features and for selected features if they are numeric values, they are being standardized and if they are categorical values they are being one-hot-encoded. 

# Exploratory data analysis

We're exploring our raw dataset for training, trying to identify outliers, fill in the missing values by using various strategies, understanding distribution across the columns, calculating correlations and visualizing our dataset.

You may open the notebook on the github or if you're having rendering problems you may use [Jupyter's online nbviewer](https://nbviewer.jupyter.org/): [belgrade_flats_for_sale_eda.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/modeling/eda/belgrade_flats_for_sale_eda.ipynb)

# Multiple Linear Regression

Multiple linear regression hypothesis: `h(x) = Wo + W1*W1 + ... + Wn*Wn`, where:
- W = weights
- X = features vector


We're implementing multiple linear regression from scatch. For finding a minimum of a cost/score function and updating coefficients, model implementation uses `batch gradient descent`.

As a baseline model for comparing with our cusom one, linear regression model is trained and used from sklearn library.

For model evaluation, on the test set, we're using `R-squared metric`.
Results on a test set (R-squared score):
.| Sklearn | Custom |
--- |--- | --- |
**R-squared**| 0.688 | 0.679 |

You may open the notebooks on the github or if you're having rendering problems you may open it via nbviewer:
- [linear_regression_sklearn.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/modeling/linear_regression/linear_regression_sklearn.ipynb)
- [linear_regression_custom.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/modeling/linear_regression/linear_regression_custom.ipynb)

# Multiclass Kernel SVM

Hypothesis for linear SVM: `h(x) = W^T*X + b` , where:
- W = weights
- b = bias term
- X = features vector.

Hypothesis in dual formulation: `h(Xk) = Sum[Xsv](alpha(i) * y(i) * K(Xk, Xsv)) + b` , where:
- Xsv = support vectors (subset of observation from a training set)
- alpha(i) = coefficients (non zero values only for support vectors)
- y(i) = output label
- K(Xk, Xsv) = kernel function, calculating dot product of vectors in a higher dimension 
- b = bias term.

In this section you may find implementation of a  `multiclass kernel SVM classification` using many binary SVM classifiers in the background. `One-to-many` scheme of a binary classifiers are use to create multiclass SVM. Output category is determined by the maximum distance from the hyperplane.

If the liner kernel is chosen, only dot product is calculated. And in case of any other kernel functions, alfa parameters are not equeal to zero only for support vectors, so we are calulating hypothesis based on dual formulation.

Implemention of a binary classificator using support vectors with kernel functions, for `marging maximization` with conditions (optimisation problem) is solved with `cvxopt library` (convex optimisation). Cvxopt library would return us an alpha coefficients for support vectors.

We have implementation of a different kernel functions:
- Linear kernel: K(x,z) = XZ
- Gaussian kernel (RBF): e^(-gamma * ||X-Z||^2)
- Polynomial kernel: K(x,z) = (C + gamma * XZ)^d

For evaluation of our cutom model, we are using trained models from sklearn library that will serve as a baseline models for us. The one that had a best performace was the one with Gaussian kernel. As a measure of performance, we're calculating accuracy and macro-F1-measure on a testing set from a confustion matrix:
. | Sklearn SVM | Custom SVM
--- | --- | ---
**Accuracy** | 0.60 | 0.56
**F1-measure** | 0.56 | 0.54

You may open the notebooks on the github or if you're having rendering problems you may open it via nbviewer:
- [svm_sklearn.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/modeling/classification/svm_sklearn.ipynb)
- [svm_custom.ipynb](https://nbviewer.jupyter.org/github/krivi95/real-estate-market-analysis/blob/master/src/modeling/classification/svm_custom.ipynb)






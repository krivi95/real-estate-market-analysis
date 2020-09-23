# Third party library imports
import numpy as np 

class Kernel:
	"""
	Utility class containing different kernel functions that could be used for 
	"""

	def __init__(self, kernel='rbf', polynomial_constant=1, gamma=10, polynomial_degree=2):
		"""
		Initializes SVM class with required parameters for training the model.

		Params:
		kernel -> one of the available kerner functions: linear, rbf or poly.
		gamma -> gamma constant for rbg kernel, if chosen.
		polynomial_constant -> constant for polynomial kernel, if chosen.
		polynomial_degree -> polynomial_degree of polynomial kernel, if chosen.
		"""
		self.kernel = kernel
		self.polynomial_constant = float(1)
		self.gamma = float(gamma)
		self.polynomial_degree = polynomial_degree

	def calculate(self, x, z):
		"""Calculates kernel function based on the specified kernel."""
		if self.kernel == 'linear':
			return self._linear_kernel(x, z)
		elif self.kernel == 'rbf':
			return self._rbf_kernel(x, z)
		elif self.kernel == 'poly':
			return self._polynomial_kernel(x, z)
			
	def _linear_kernel(self, x, z):
		"""
		Linear kernel function.
		Formula: K(x,z) = XZ
		"""
		return np.dot(x.T, z)

	def _polynomial_kernel(self, x, z):
		"""
		Polynomial kernel function.
		Formula: K(x,z) = (C + gamma * XZ)^d
		"""
		return (self.polynomial_constant + self.gamma * np.dot(x.T,z))**self.polynomial_degree

	def _rbf_kernel(self, x, z):
		"""
		Gaussian RBF (Radial Basis Funcion).
		Formula: K(x,z) = e^(-gamma * ||X-Z||^2)
		"""
		return np.exp(-1.0 * self.gamma * np.dot(np.subtract(x, z).T, np.subtract(x, z)))


class SVM():
	"""
	Class implementing binary classification using Support Vectors with kernel functions.
	Marging minimization with conditions (optimisation problem) is solved with cvxopt (convex optimisation).
	"""

	def __init__(self, kernel="rbf", polynomial_constant=1, gamma=10, polynomial_degree=2):
		"""
		Initializes SVM class with required parameters for training the model.

		Params:
		kernel -> one of the available kerner functions: linear, rbf or poly.
		gamma -> gamma constant for rbg kernel, if chosen.
		polynomial_constant -> constant for polynomial kernel, if chosen.
		polynomial_degree -> polynomial_degree of polynomial kernel, if chosen.
		"""
		# Creating selected kernel for SVM
		self.kernel = kernel
		self.kernel_function = Kernel(kernel, polynomial_constant, gamma, polynomial_degree)

		# Support vectors data		
		self._support_vectors = None 	# Observations from training set (X) that are SVs
		self._support_labels = None		# Observations from training set (Y) for SVs
		self._alphas = None 			# Alpha coefficients for SVs
		self._indices = None			# Support vector indices in training set  

		self.b = 0						# Bias term (W0)
		self.weights = None				# Weights for linear hypothesis: h(x) = W^T*X + b



	def signature(self, X):
		"""
		Returns sign of given predictions.
		
		Params:
		X -> np.array containing distances from hyperplane.
		"""
		return np.where(X>0, 1, -1)

	def hypothesis(self, X):
		"""
		For each given observations, calculates SVM hypothesis - h(X).
		If the liner kernel is chosen, only dot product is calculated.
		And in case of any other kernel functions, alfa parameters are not equeal to zero only for support vectors, 
		so we are calulating hypothesis based on dual formulation:
		h(Xk) = Sum[Xsv](alpha(i) * y(i) * K(Xk, Xsv)) + b.

		Params:
		X -> matrix with features (shape: number of observations X number of features in model)
		"""
		if self.kernel=="linear":
			hypothesis = np.dot(X, self.weights) + self.b
		else:
			hypothesis = np.zeros(X.shape[0])
			for i in range(X.shape[0]):
				# Calculate hypothesis for each given set of features
				h = 0
				for alpha, y, X_sv in zip(self._alphas, self._support_labels, self._support_vectors):
					h += alpha * y * self.kernel_function.calculate(X[i], X_sv)
				hypothesis[i] = h
			hypothesis = hypothesis + self.b
		return hypothesis

	def predict(self, X):
		"""
		Creates binary prediction (-1, +1) for given observations.
		
		Params:
		X -> matrix with features (shape: number of observations X number of features in model).
		"""
		return self.signature(self.hypothesis(X))


class MulticlassSVM:
	"""
	Class implementing multiclass classification using many binary SVM classifiers in the background.
	One-to-many binary classifiers are use to create multiclass SVM.
	Output category is determined by the maximum distance from the hyperplane.
	"""

	def __init__(self, kernel="rbf", polynomial_constant=1, gamma=10, polynomial_degree=2):
		"""
		Initializes multiclass SVM. Kernel parameters are use to create individual kernel SVMs.

		Params:
		kernel -> one of the available kerner functions: linear, rbf or poly.
		gamma -> gamma constant for rbg kernel, if chosen.
		polynomial_constant -> constant for polynomial kernel, if chosen.
		polynomial_degree -> polynomial_degree of polynomial kernel, if chosen.
		"""
		self.kernel = kernel
		self.polynomial_constant = float(1)
		self.gamma = float(gamma)
		self.polynomial_degree = polynomial_degree

	def _get_nummber_of_categories(self, labels):
		"""
		Returns the number of classes from provided label output.
		
		Params:
		labels -> provided aray containing labels for training set.
		"""
		return len(np.unique(labels))
    
	def _is_binary_classification(self, labels):
		"""
		Returns the info if the classification is multiclass or binary, 
		depending on number of unique categories under labeles, for training set.
		"""
		if self._get_nummber_of_categories(labels) == 2:
			return True
		return False

	def _create_one_vs_many_labels(self):
		"""
		Creates new output labes, one for each of the one-to-many binary classifiers.
		(Labels for the current binary classifier is changed to 1 and all the other labels are changed to -1).
		"""
		for label in np.unique(self.y):
				self.labels[label] = np.copy(self.y)
				self.labels[label][self.labels[label] != label] = -1
				self.labels[label][self.labels[label] == label] = 1

	def _fit_one_vs_many_classifiers(self):
		"""Based on the number of classes we have, we are training the same number of binary one-to-many classifiers."""
		for label in self.labels:
			print(f'Fitting one-to-many SVM binary classifier for class: {label}')
			self.classifiers[label] = SVM(kernel=self.kernel, polynomial_constant=self.polynomial_constant, gamma=self.gamma, polynomial_degree=self.polynomial_degree)
			self.classifiers[label].fit(self.X, self.labels[label])
		
	def fit(self, X, y):
		"""
		Fits the multiclass SVM model by creating multiple classifiers, using one-vs-many approach.
		
		Params:
		X -> training set, containing features (shape: number of observations X number of features in model).
		y -> output labels for training set.
		"""
		self.X = X
		self.y = y
		self.labels = {}
		self.classifiers = {}
		self.num_of_categories = self._get_nummber_of_categories(y)
		if self._is_binary_classification(y):
			# There are only two categories in provided training results - binary classification
			raise Exception('Provided binary output labels. Please use SVM class for binary classification.')
		else:
			# There are more that two categories in provided training results - multiclass svm (one-vs-many approach)
			print(f'Provided multiclass output labels. Creating {self.num_of_categories} binary classificators...')
			
			# Creating separate output labels for different binary classifiers
			self._create_one_vs_many_labels()
			
			# Training different binary classifiers
			self._fit_one_vs_many_classifiers()
			
	def predict(self, X):
		"""
		Creating predictions based on the maximum distance from hyperplane, accross all one-to-many binary classifiers.
		
		Params:
		X -> matrix with features (shape: number of observations X number of features in model)
		"""
		# Creating predictions for each binary classifier
		predictions = {}
		for label in self.classifiers:
			predictions[label] = self.classifiers[label].hypothesis(X)

		# Determining the class based on a maximun distance from a hyperplane
		y = []
		for p0, p1, p2, p3, p4 in zip(predictions[0], predictions[1], predictions[2], predictions[3], predictions[4]):
			single_observation_predictions = [p0, p1, p2, p3, p4]
			y.append(single_observation_predictions.index(max([p0, p1, p2, p3, p4])))
		return y
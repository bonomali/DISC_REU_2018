#!/usr/bin/python
"""The goal of this script is to build a 3-layer neral network with one input layer, one hidden layer, and one output layer, using gradient descent.
	The numer of nodes in the input layer is determined by the dimensinoality of our data, i.e. 2 (X[:,0] and X[:,1])
	Similarly, the output layer node number is determined by the number of classes we have; i.e. 2 (blue vs pink in plot).
	We can choose the dimensionality (number of nodes) of the hidden layer. The more nodes we put in, the more complex functions we can fit; but they come at a cost of e.g. overfitting.
	Also need an activation function for hiddin layer. Activation function transforms the inputs of the layer into its outputs. A nonlinear activation functino is what allows us to fit nonlinear hypotheses. Common choices for activation functions are tanh or sigmoid. 
	We will use tanh, which performs quite well in many scenarios.
	A nice property of these functions is that their derivative can be computed using the original function value; e.g. derivative of tanh x is 1 - tanh^2x.
	Because we want our network to output probablities, the acivation function for the output layer will be the softmax, which is simply a way to convert raw scores to probabilities.

	We also need a loss function to test errors -- i.e. add to it if our classification doesn't match the true classification.
	As an input, our gradient descent needs the gradients of the loss function wrt our parameters. To calculate these gradients we use the famous backpropagation algorithm, which is a way to efficently calculate the gradients starting from the output."""

import matplotlib.pyplot as plt 
import numpy as np 
import sklearn 
import sklearn.datasets 
import sklearn.linear_model 
import matplotlib 

#Generate a dataset and plot it
np.random.seed(0)
X, y = sklearn.datasets.make_moons(200, noise=0.20)
plt.scatter(X[:,0], X[:,1], s=40, c=y, cmap = plt.cm.Spectral)

#Start by defining useful variables and parameters for gradient descent:
num_examples = len(X[:,0]) # training set size
nn_input_dim = 2 #input layer dimensionality
nn_output_dim= 2 #output layer dimensionality

#Gradient descent parameters -- just pick by hand
epsilon = 0.01		#learning rate for gradient descent
reg_lambda = 0.01	#regularisation strength

"""Function to evaluate total loss on the dataset"""
def calculate_loss(model):
	W1, b1, W2, b2 = model["W1"], model["b1"], model["W2"], model["b2"]
	#forward propagation to calculate our predictions, where zi is input to layer i, ai is output of layer i (input x activation function)
	z1 = X.dot(W1) + b1
	a1 = np.tanh(z1)
	z2 = a1.dot(W2) + b2
	exp_scores = np.exp(z2)
	probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)
	#Calculating the loss
	correct_logprobs = -np.log(probs[range(num_examples), y])
	data_loss = np.sum(correct_logprobs)
	#add regularisation term to loss (optional, stops overfitting)
	data_loss += reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
	return 1./num_examples * data_loss

"""Function to predict an output (0 or 1)"""
def predict(model, x):
	W1, b1, W2, b2 = model["W1"], model["b1"], model["W2"], model["b2"]
	#forward propagation to calculate our predictions, where zi is input to layer i, ai is output of layer i (input x activation function)
	z1 = x.dot(W1) + b1
	a1 = np.tanh(z1)
	z2 = a1.dot(W2) + b2
	exp_scores = np.exp(z2)
	probs = exp_scores / np.sum(exp_scores, axis = 1, keepdims = True)
	return np.argmax(probs, axis=1)

"""Finally, function to train neural network; implements batch gradient descent using backpropagation derivatives."""
# nn_hdim: number of nodes in the hidden layer
# num_passes: number of passes through the training data for gradient descent
# print_loss: if True, print the loss ever 1000 iterations
def build_model(nn_hdim, num_passes=20000, print_loss=False):
	#Initialise the parameters to random values. Need to learn these.
	np.random.seed(0)
	W1 = np.random.randn(nn_input_dim, nn_hdim) / np.sqrt(nn_input_dim)
	b1 = np.zeros((1, nn_hdim))
	W2 = np.random.randn(nn_hdim, nn_output_dim)/ np.sqrt(nn_hdim)
	b2 = np.zeros((1, nn_output_dim))
	
	#This is what we return at the end
	model = {}
	
	#Gradient descent. For each batch:
	for i in xrange(0, num_passes):
		#Forward propagation
		z1 = X.dot(W1) + b1
		a1 = np.tanh(z1)
		z2 = a1.dot(W2) + b2
		exp_scores = np.exp(z2)
		probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
		
		#backpropagation. Note .T => transpose.
		delta3 = probs
		delta3[range(num_examples), y] -=1
		dW2 = (a1.T).dot(delta3)
		db2 = np.sum(delta3, axis=0, keepdims=True)
		delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
		dW1 = np.dot(X.T, delta2)
		db1 = np.sum(delta2, axis=0)
		
		#Add regularisation terms (b1 and b2 don't have regularisation terms)
		dW2 += reg_lambda *W2
		dW1 += reg_lambda *W1
		
		#Gradient descent parameter update
		W1 += -epsilon * dW1
		b1 += -epsilon *db1
		W2 += -epsilon *dW2
		b2 += -epsilon *db2
		
		#Assign new parameters to the model
		model = { 'W1': W1, 'b1':b1, 'W2':W2, 'b2':b2}
		
		#optionally print the loss.
		#Computationally expensive because it uses the whole dataset, so don't do it too frequently.
		if print_loss and i %1000 == 0:
			print "Loss after iteration %i: %f" %(i, calculate_loss(model))
	return model

"""Used to generate contour diagram of plot"""
def plot_decision_boundary(pred_func): 
	# Set min and max values and give it some padding 
	x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5 
	y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5 
	h = 0.01 
	# Generate a grid of points with distance h between them 
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h)) 
	# Predict the function value for the whole gid 
	Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
	Z = Z.reshape(xx.shape) 
	# Plot the contour and training examples 
	plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral) 
	plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral) 

#Now let's see what happens if we train a network with a hidden layer size of 3.

#Build a model with a 3D hidden layer
model = build_model(3, print_loss = True)
plt.figure()
plot_decision_boundary(lambda x: predict(model, x))
plt.title("Decision boundary for hidden layer size 3")

model = build_model(10, print_loss = True)
plt.figure()
plot_decision_boundary(lambda x: predict(model, x))
plt.title("Decision boundary for hidden layer size 10")

model = build_model(6, print_loss = True)
plt.figure()
plot_decision_boundary(lambda x: predict(model, x))
plt.title("Decision boundary for hidden layer size 6")

model = build_model(2, print_loss = True)
plt.figure()
plot_decision_boundary(lambda x: predict(model, x))
plt.title("Decision boundary for hidden layer size 2")

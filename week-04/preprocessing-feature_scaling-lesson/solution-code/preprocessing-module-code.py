from sklearn.datasets import load_iris

iris = load_iris()

print iris.data
print iris.target

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=314)

print x_train.size, x_test.size

from sklearn.preprocessing import Binarizer
import numpy as np

binary = Binarizer(np.mean(x_train[:,0]))

print binary

binary.fit(x_train[:,0])

print binary.transform(x_train[:,0])
print np.mean(binary.transform(x_train[:,0])) ## What percent of train is above the mean?

print np.mean(binary.transform(x_test[:,0])) ## Transform X_Test

# What happens if I refit binary?

binary = Binarizer(np.mean(x_test[:,0]))
binary.fit(x_test[:,0])
print np.mean(binary.transform(x_test[:,0]))

print np.mean(x_train[:,0]), np.mean(x_test[:,0])

#####

def get_first_column(data):
	return data[:,0].reshape(-1, 1)

print get_first_column(x_train)

from sklearn.preprocessing import FunctionTransformer

ft = FunctionTransformer(get_first_column)

print ft.fit_transform(x_train)

def stupid_scaler(data):
	column = data[:,0]
	avg = np.mean(column)
	values = column - avg
	return values.reshape(-1, 1)

ft_weird = FunctionTransformer(stupid_scaler)

print ft_weird.fit_transform(x_train)

###

fake_data = np.array([1, 1, 1, 5, 2, 7, 2, 2, 0, 1, 2, 3]).reshape(-1,1)

print fake_data

from sklearn.preprocessing import LabelBinarizer 

lb = LabelBinarizer()

print lb.fit_transform(fake_data)

print fake_data.shape
print lb.fit_transform(fake_data).shape

# If we fed in some "test data" we could get back values for those dummies

fake_test_data = np.array([2, 4, 0, 1, 1, 0, 8, 9]).reshape(-1,1)

print lb.transform(fake_test_data)

print len(set([1, 1, 1, 5, 2, 7, 2, 2, 0, 1, 2, 3]))

print lb.classes_ # Here are column names

####

fake_data = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)

from sklearn.preprocessing import PolynomialFeatures

pf = PolynomialFeatures(3, include_bias=False)

print fake_data
print pf.fit_transform(fake_data)
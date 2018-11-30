from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import sklearn as sk
import pandas as pd 
from sklearn.model_selection import StratifiedKFold
import numpy as np

data = pd.read_csv("../features_alpha.csv").values
labels = pd.read_csv("../labels.csv", header=None).values

print(data.shape[0], labels.shape[0])

folds = StratifiedKFold(n_splits=10)

accuracy = []
precision = []
recall = []
kappa = []

model = SVC()

for train_index, test_index in folds.split(data, labels):
	X_train, X_test = data[train_index], data[test_index]
	y_train, y_test = labels[train_index], labels[test_index]

	model.fit(X_train, y_train)

	y_predicted = model.predict(X_test)

	accuracy.append(sk.metrics.accuracy_score(y_test, y_predicted))
	precision.append(sk.metrics.precision_score(y_test, y_predicted, average=None)[1])
	recall.append(sk.metrics.recall_score(y_test, y_predicted, average=None)[1])
	kappa.append(sk.metrics.cohen_kappa_score(y_test, y_predicted))

print('{:.1%}'.format(np.mean(accuracy)) + "," + '{:.3%}'.format(np.std(accuracy)) + ",")
print('{:.1%}'.format(np.mean(precision)) + "," + '{:.3%}'.format(np.std(precision)) + ",")
print('{:.1%}'.format(np.mean(recall)) + "," + '{:.3%}'.format(np.std(recall)) + ",")
print('{:.2f}'.format(np.mean(kappa)) + "," + '{:.2f}'.format(np.std(kappa)) + "\n")

import numpy as np
from sklearn import svm
from sklearn.cross_validation import train_test_split

def svm_baseline():
    data = np.genfromtxt('connect-4.data.converted', delimiter=',', dtype=None)
    X = data[:,0:-1]
    y = data[:,-1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

    clf = svm.SVC()
    clf.fit(X_train, y_train)

    predictions = [int(a) for a in clf.predict(X_train)]
    num_correct = sum(int(a == y) for a, y in zip(predictions, y_train))

    print "Baseline classifier using an SVM."
    print "%s of %s values correct." % (num_correct, len(y_train))

if __name__ == "__main__":
    svm_baseline()

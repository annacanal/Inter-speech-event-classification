from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn import preprocessing
import numpy as np
import data_handling, os, json
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
import itertools
import matplotlib
from matplotlib import pyplot as plt



# Those are used when assuming existing reduction, and not exploring new
PERPLEXITY = 50
LEARNING_RATE = 300
EXAGGERATION = 84


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Greys):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes,fontsize=15, rotation=45)
    plt.yticks(tick_marks, classes,fontsize=15)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",fontsize=22,
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label',fontsize=15)
    plt.xlabel('Predicted label',fontsize=15)


def main():
    names = data_handling.read_names(["keynote"])
    samples, targets, zero_length_indices = data_handling.dataset(names)
    names = np.delete(names, zero_length_indices)
    # Samples Preprocessing
    samples = data_handling.scale_select(samples)



    # Class balancing
    # data = data_handling.balance_classes(data)
    # print("Balanced data shape: {}".format(np.shape(data)))
    # samples = data[:, :-1]
    # targets = data[:, -1]
    # unique, counts = np.unique(targets, return_counts=True)
    # print("Class breakdown: {}\n".format(dict(zip(unique, counts))))

    #output_file
 #   data_handling.output_files_labels_case_study(names, targets, data_root2)
    unique, counts = np.unique(targets, return_counts=True)
    print("The case study data are broken into classes like so: {}".format(dict(zip(unique, counts))))

    #### CROSS validation



    print("Perplexity: {}".format(PERPLEXITY))
    #Reduction
    #reduced_samples = data_handling.tsne_reduction(samples, PERPLEXITY, l_r=LEARNING_RATE)
    #print("Reduced samples shape: {}".format(np.shape(reduced_samples)))
    ########
    data = np.hstack((samples, np.reshape(targets, (len(targets), 1))))
    #data = np.hstack((reduced_samples, np.reshape(targets, (len(targets), 1))))
    #data = data_handling.balance_classes(data)

    clf = SVC(C=1, class_weight='balanced', verbose=0, probability=True)
    #cv = ShuffleSplit(n_splits=1, test_size=0.8, random_state=0)
    score1 = cross_val_score(clf,data[:, :-1], data[:, -1], cv=5, scoring='accuracy')
   # score1 = cross_val_score(clf, reduced_samples, targets, cv=5, scoring='accuracy')
    print("Cross validation (accuracy) score")
    print(score1)
    print("average:")
    print(np.average(score1))
    print("std:")
    print(np.std(score1))
    score2 = cross_val_score(clf,data[:, :-1], data[:, -1], cv=5, scoring='precision_macro')
    #score2 = cross_val_score(clf, reduced_samples, targets, cv=5, scoring='precision_macro')
    print("Cross validation (precision) score")
    print(score2)
    print("average:")
    print(np.average(score2))
    print("std:")
    print(np.std(score2))
    score3 = cross_val_score(clf,data[:, :-1], data[:, -1], cv=5, scoring='recall_macro')
  #  score3 = cross_val_score(clf, reduced_samples, targets, cv=5, scoring='recall_macro')
    print("Cross validation (recall) score")
    print(score3)
    print("average:")
    print(np.average(score3))
    print("std:")
    print(np.std(score3))


    # Split in train and test
    train, test, train_targets, test_targets = train_test_split(samples,targets, test_size=0.1, random_state=1337)
    #train, test, train_targets, test_targets = train_test_split(reduced_samples, targets, test_size=0.1, random_state=1337)
    print("shape train: {}".format(np.shape(train)))
    print("shape test: {}".format(np.shape(test)))

    clf = SVC(C=1, class_weight='balanced', verbose=0, probability=True)
    #clf.fit(train[:, :-1], train[:, -1])
    clf.fit(train, train_targets)


    # #### Try on Keynote#########
    print("Train confusion matrix=")
    predictions_train = clf.predict(train)
    cnf_train = confusion_matrix(train_targets, predictions_train, labels=["silences", "breathing", "clicks"])
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    plot_confusion_matrix(cnf_train, classes=["silences", "breathing", "clicks"], normalize=True,
                          title='Train confusion matrix normalized')
    print("Test confusion matrix=")
    #predictions_test= clf.predict(test[:, :-1])
    predictions_test = clf.predict(test)
    cnf_test=confusion_matrix(test_targets, predictions_test, labels=["silences", "breathing", "clicks"])

    ax2 = fig.add_subplot(122)
    plot_confusion_matrix(cnf_test, classes=["silences", "breathing", "clicks"],normalize=True,
                          title='Test confusion matrix normalized')

    # print("confusion matrix=")
    # predictions = clf.predict(data[:, :-1])
    # cnf = confusion_matrix(data[:, -1], predictions, labels=["silences", "breathing", "clicks"])
    # #fig = plt.figure()
    # ax3 = fig.add_subplot(122)
    # plot_confusion_matrix(cnf, classes=["silences", "breathing", "clicks"], normalize=True,
    #                       title=' confusion matrix normalized')
    plt.show()



 #   data_handling.output_files_labels(names, predictions,data_root2)



if __name__ == "__main__":
    main()
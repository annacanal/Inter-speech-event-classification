from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from sklearn import preprocessing
import numpy as np
import data_handling, os, json
import data_handling2
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
import itertools

import matplotlib
# matplotlib.use('agg')
from matplotlib import pyplot as plt

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

    # print("Perplexity: {}".format(PERPLEXITY))
    # print("Learning Rate: {}".format(LEARNING_RATE))
    # Reduction
    # reduced_samples = data_handling.tsne_reduction(samples, PERPLEXITY, l_r=LEARNING_RATE)
    # print("Reduced samples shape: {}".format(np.shape(reduced_samples)))

    data = np.hstack((samples, np.reshape(targets, (len(targets), 1))))
    # data = np.hstack((reduced_samples, np.reshape(targets, (len(targets), 1))))
    unique, counts = np.unique(targets, return_counts=True)
    print("The case study data are broken into classes like so: {}".format(dict(zip(unique, counts))))




 ###train with all keynote data
    clf = SVC(C=1, class_weight='balanced', verbose=0, probability=True)
    clf.fit(data[:, :-1], data[:, -1])

    # ############ Try on GECO ############
    print("Using the SVC trained on the case study to classify the GECO")
    names1 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["A", "C"])])
    samplesGe1, _, _ = data_handling.dataset(names1)
    names2 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["A", "K"])])
    samplesGe2, _, _ = data_handling.dataset(names2)
    names3 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["B", "A"])])
    samplesGe3, _, _ = data_handling.dataset(names3)
    names4 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["B", "M"])])
    samplesGe4, _,_ = data_handling.dataset(names4)
    names5 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["C", "E"])])
    samplesGe5, _,_ = data_handling.dataset(names5)
    names6 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["C", "F"])])
    samplesGe6, _,_ = data_handling.dataset(names6)
    names7 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["D", "G"])])
    samplesGe7, _,_ = data_handling.dataset(names7)
    names8 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["D", "L"])])
    samplesGe8, _,_ = data_handling.dataset(names8)
    names9 = data_handling.read_names(["geco", data_handling.get_conversation_directory(["E", "I"])])
    samplesGe9, _, _ = data_handling.dataset(names9)
    samples_tot = np.concatenate((samplesGe1, samplesGe2,samplesGe3,samplesGe4,samplesGe5,samplesGe6,samplesGe7,samplesGe8,samplesGe9),axis=0)
    names = np.concatenate((names1, names2,names3,names4,names5,names6,names7,names8,names9),axis=0)

    print("Original shapes, samples: {}".format(np.shape(samples_tot)))
    # Preprocessing
    samples_tot = data_handling.scale_select(samples_tot)
    print("Feature selection shapes, samples: {}".format(np.shape(samples_tot)))

    # Reduction
    # reduced_samples_tot = data_handling.tsne_reduction(samples_tot, PERPLEXITY, l_r=LEARNING_RATE)
    # print("Reduced samples shape: {}".format(np.shape(reduced_samples)))
    # ###########

    print("The GECO data are shaped: {}".format(np.shape(samples_tot)))
    predictions = clf.predict(samples_tot)
    # predictions = clf.predict(reduced_samples_tot)
    print("Predictions: {}".format(np.shape(samples_tot)))

    # labels have to be given by zofia
    # cnf_test = confusion_matrix(labels_geco[:, -1], predictions, labels=["silences", "breathing", "clicks"])
    # fig = plt.figure()
    #
    # plot_confusion_matrix(cnf_test, classes=["silences", "breathing", "clicks"], normalize=True,
    #                       title='Test confusion matrix normalized')
    # plt.show()

    data_handling.output_GECO_files_labels(names, predictions)



    unique, counts = np.unique(predictions, return_counts=True)
    print("The GECO predictions are broken into classes like so: {}".format(dict(zip(unique, counts))))


if __name__ == "__main__":
    main()
from sklearn.svm import SVC

import numpy as np
import data_handling, os, logger, preprocessing, tSNE_IO

import matplotlib
from matplotlib import pyplot as plt

# Those are used when assuming existing reduction, and not exploring new
PERPLEXITY = 30
LEARNING_RATE = 600
EXAGGERATION = 84

def plotting(data, title, clf):
    plt.axis('tight')
    h = .02
    x_min = data[:, 0].min() - 1
    x_max = data[:, 0].max() + 1
    y_min = data[:, 1].min() - 1
    y_max = data[:, 1].max() + 1

    print("Checkpoint 1")
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    print("Checkpoint 2")
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
            extent=(xx.min(), xx.max(), yy.min(), yy.max()),
            cmap=plt.cm.Paired,
            aspect='auto', origin='lower')

    print("Checkpoint 3")
    plt.scatter(data[:, 0], data[:,1], color = 'black', marker = '.', linewidths=0)

    plt.title("{}".format(title))
    plt.savefig(os.path.join(data_handling.results_root, "img", "graphs", title))
    # plt.show()


def main():
    names= data_handling.read_names(["keynote"])
    samples, targets, zero_length_indices = data_handling.dataset(names)
    names = np.delete(names, zero_length_indices)

    print("Original shapes, samples: {} \t targets : {} \t names: {}".format(np.shape(samples), np.shape(targets), np.shape(names)))
    unique, counts = np.unique(targets, return_counts = True)
    print("Class breakdown: {}".format(dict(zip(unique, counts))))

    # Samples Preprocessing
    samples = preprocessing.scale_select(samples)
    print("Feature selection shapes, samples: {} \t targets : {}\n".format(np.shape(samples), np.shape(targets)))
    # ###########

    # Dimensionality reduction and classification exploration
    if(False):
        dimensionalities = [100, 150, 170, 200]
        perplexities = [35, 40, 45, 50]
        learning_rates = [500, 800]
        for dimensionality in dimensionalities:
            for perplexity in perplexities:
                for l_r in learning_rates:
                    print("Dimensionality: {} \t Perplexity: {} \t Learning rate : {}".format(dimensionality, perplexity, l_r))

                    # Reduction
                    print("Reduction")
                    reduced_samples = tSNE_IO.load_or_reduce(samples)
                    print("Reduced samples shape: {}".format(np.shape(reduced_samples)))
                    # ########

                    # Class balancing
                    data = np.hstack((reduced_samples, np.reshape(targets, (len(targets), 1))))
                    data, names = preprocessing.balance_classes(data, names, np.shape(reduced_samples)[1])
                    print("Balanced data shape: {}".format(np.shape(data)))
                    reduced_samples = data[:, :-1]
                    targets = data[:, -1]
                    unique, counts = np.unique(targets, return_counts = True)
                    print("Class breakdown: {}\n".format(dict(zip(unique, counts))))
                    # ###########

                    # Splitting
                    # Split in train and test
                    train, test = preprocessing.split(reduced_samples, targets, 0.15)
                    # #########
                    for c in np.arange(.1, .9, .1):
                        # SVM fitting
                        clf = SVC(C = c, class_weight = 'balanced', verbose = 0, probability = True)

                        clf.fit(train[:, :-1], train[:, -1])
                        score = clf.score(test[:, :-1], test[:, -1])

                        print("SVC score of fit on case study data: {}, with C: {}".format(score, clf.get_params()["C"]))

                        parameters = {
                                "algo" : "SVC",
                                "kernel" : clf.get_params()["kernel"],
                                "dataset" : "keynote",
                                "tsne_perplexity" : perplexity,
                                "tsne_learning_rate" : l_r,
                                "tnse_dimensionality" : dimensionality,
                                "svc_c" : c,
                                "score" : score,
                        }

                        logger.store_log_entry(parameters, "keynote_supervised_exploration_log.json")
            print()

    # Assume dimensionality reduction, classification exploration
    if(True):
        # Reduction
        print("Reduction")
        reduced_samples = tSNE_IO.load_or_reduce(samples, PERPLEXITY, LEARNING_RATE, EXAGGERATION)
        print("Reduced samples shape: {}".format(np.shape(reduced_samples)))
        # ########

        # Class balancing
        data = np.hstack((reduced_samples, np.reshape(targets, (len(targets), 1))))
        data, names = preprocessing.balance_classes(data, names, np.shape(reduced_samples)[1])
        print("Balanced data shape: {}".format(np.shape(data)))
        reduced_samples = data[:, :-1]
        targets = data[:, -1]
        unique, counts = np.unique(targets, return_counts = True)
        print("Class breakdown: {}\n".format(dict(zip(unique, counts))))
        # ###########

        # Split in train and test
        train, test = preprocessing.split(reduced_samples, targets, 0.15)
        # #########

        for c in np.arange(.1, 1, .1):
            # SVM fitting
            clf = SVC(C = c, class_weight = 'balanced', verbose = 0, probability = True)

            clf.fit(train[:, :-1], train[:, -1])
            score = clf.score(test[:, :-1], test[:, -1])

            print("SVC score of fit on case study data: {}, with C: {}".format(score, clf.get_params()["C"]))

            parameters = {
                    "algo" : "SVC",
                    "kernel" : clf.get_params()["kernel"],
                    "dataset" : "keynote",
                    "tsne_perplexity" : PERPLEXITY,
                    "tsne_learning_rate" : LEARNING_RATE,
                    "tnse_dimensionality" : 2,
                    "svc_c" : c,
                    "score" : score,
            }

            logger.store_log_entry(parameters, "keynote_supervised_exploration_log.json")

if __name__ == "__main__":
    main()
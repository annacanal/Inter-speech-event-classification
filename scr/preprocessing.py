from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn import preprocessing
# from sklearn import manifold
from MulticoreTSNE import MulticoreTSNE as TSNE
from sklearn.feature_selection import VarianceThreshold

import numpy as np
import operator, data_handling

def scale_select(samples):
    samples = preprocessing.scale(samples)
    feature_selector = VarianceThreshold()
    samples = feature_selector.fit_transform(samples)

    return samples

def robust_scale_select(samples):
    samples = preprocessing.robust_scale(samples)
    feature_selector = VarianceThreshold()
    samples = feature_selector.fit_transform(samples)

    return samples


def balancing(samples, targets):
    data = np.hstack((samples, np.reshape(targets, (len(targets), 1))))
    data = balance_classes(data)

    return data

def tsne_reduction(samples, perplexity, data = None, n_components = 2, l_r = 200, dim = 2, ex = 12, iterations = 5000, verbosity = 0):
    if(samples is None) and (data is not None):
        samples = data[:, :-1]
        targets = data[:, -1]

    # tsne = manifold.TSNE(n_components = dim, init='pca', learning_rate = l_r, 
    #                         perplexity=perplexity, early_exaggeration = ex,
    #                         n_iter = iterations, random_state=data_handling.RANDOM_SEED,
    #                         verbose = verbosity)

    tsne = TSNE(n_components = dim, n_jobs = -1, learning_rate = l_r, 
                            perplexity=perplexity, early_exaggeration = ex,
                            n_iter = iterations, random_state=data_handling.RANDOM_SEED,
                            verbose = verbosity)

    reduced_samples = tsne.fit_transform(samples)

    return reduced_samples, tsne

def split(samples, targets, size):
    data = np.hstack((samples, np.reshape(targets, (len(targets), 1))))
    train, test = train_test_split(data,test_size=size, random_state =data_handling.RANDOM_SEED)

    return train, test


# Gets the samples with stacked targets as input
def balance_classes(data, names, features):
    if np.shape(data)[1] != features+1:
        raise ValueError("Data must consist of the samples and the target stacked to the end of each sample.")

    unique, counts = np.unique(data[:, -1], return_counts = True)

    class_samples = []
    names_by_class = []
    for _ in unique:
        names_by_class.append([])
        class_samples.append(list())

    for i, sample in enumerate(data):
        target = int(sample[-1])

        if len(class_samples[target]) == 0:
            class_samples[target]

        if target in [0, 1, 2]:
            class_samples[target].append(sample)
            names_by_class[target].append(names[i])
        else:
            raise ValueError("Invalid class")
    
    unique, counts = np.unique(data[:, -1], return_counts = True)
    class_lengths = dict(zip(unique, counts))
    sorted_samples = sorted(class_lengths.items(), key = operator.itemgetter(1))

    class_with_most_samples = sorted_samples[-1][0]
    class_cutoff = sorted_samples[-2]

    class_to_balance = class_samples[int(class_with_most_samples)]
    names_to_balance = names_by_class[int(class_with_most_samples)]

    class_subset = np.random.choice(np.shape(class_to_balance)[0], size = int(class_cutoff[1]))
    
    balanced_class_samples = np.array(class_to_balance)[class_subset, :]
    balanced_names = np.array(names_to_balance)[class_subset]


    balanced_classes = (class_samples[int(sorted_samples[0][0])], class_samples[int(sorted_samples[-2][0])], balanced_class_samples)
    balanced_names = (names_by_class[int(sorted_samples[0][0])], names_by_class[int(sorted_samples[-2][0])], balanced_names)


    data = np.vstack(balanced_classes)
    names = [name for names in balanced_names for name in names]

    return data, names
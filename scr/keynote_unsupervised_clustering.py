from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import numpy as np

import data_handling, os, preprocessing, path_manipulations, tSNE_IO

import matplotlib
from matplotlib import pyplot as plt

PERPLEXITY = 30
LEARNING_RATE = 600
EXAGGERATION = 84


def plot_clusters(samples, targets, title, type = "predicted"):
    clustered = [[] for _ in np.unique(targets)]

    for i in range(len(samples)):
        clustered[int(targets[i])].append(samples[i])

    if type == "actual":
        labels = ["silences", "clicks", "breathing"]
        colors = ["red", "green", "blue"]
        cmap = "seismic"
    if type == "predicted":
        labels = ["cluster_{}".format(i) for i in np.unique(targets)]
        colors = []
        cmap = "RdBu"
    
    markers = [".", "*", "+"]

    for i, cluster in enumerate(clustered):
        cluster = np.array(cluster)
        if type == "actual":
            plt.scatter(cluster[:, 0], cluster[:, 1], cmap = cmap, marker = markers[i], label = labels[i])
        elif type == "predicted":
            plt.scatter(cluster[:, 0], cluster[:, 1], label = labels[i], cmap = cmap, marker = '.', linewidths = 0)

    plt.legend()
    plt.title("{} clusters".format(title))

    output_filename = "{}_clusters.png".format("_".join(title.split()))
    output_dir = path_manipulations.create_or_return([data_handling.results_root, "img", "unsupervised"])

    plt.savefig(os.path.join(output_dir, output_filename))

    plt.show()

def extract_to_file(names, samples, targets, algo = "DBSCAN"):
    if np.shape(names)[0] != np.shape(samples)[0]:
        print("names shape : {} \t samples shape: {}".format(np.shape(names), np.shape(samples)))
        raise ValueError("length of names not equal to length of samples")

    output_filename = "{}_clustering_out.csv".format(algo)
    output_dir = path_manipulations.create_or_return([data_handling.results_root,"output_files"])

    with open(os.path.join(output_dir, output_filename ), 'w') as f:
        for i, sample in enumerate(samples):
            sample_name = names[i]
            parts = sample_name.split('_')
            start = parts[4]
            end = parts[5][:-4]
            sample_label = targets[i]

            line = "{}, {}, {}, {}, {}\n".format(i, sample_name, start, end, sample_label)
            f.write(line)

    print("Output file created")

def study_clusters(samples, reduced_samples, predictions):
    clustered = [[] for _ in np.unique(predictions)]

    for i in range(len(reduced_samples)):
        clustered[int(predictions[i])].append(samples[i])

    for i, cluster in enumerate(clustered):
        print("cluster_{}".format(i))

        plt.matshow(cluster)
        plt.title("cluster_{}".format(i))
        plt.show()

        print("Mean: {}".format(np.mean(cluster, axis = 1)))
        print("STD: {}".format(np.std(cluster, axis = 1)))

def main():
    names = data_handling.read_names(["keynote"])
    samples, targets, zero_length_indices = data_handling.dataset(names)
    names = np.delete(names, zero_length_indices)


    print("Original shapes, samples: {} \t targets : {} \t names: {}".format(np.shape(samples), np.shape(targets), np.shape(names)))
    unique, counts = np.unique(targets, return_counts = True)
    print("Class breakdown: {}".format(dict(zip(unique, counts))))

    # Samples Preprocessing
    samples = preprocessing.scale_select(samples)
    print("Feature selection shapes, samples: {} \t targets : {}".format(np.shape(samples), np.shape(targets)))
    # ###########

    # tSNE Reduction
    print("Reduction")
    reduced_samples = tSNE_IO.load_or_reduce(samples, PERPLEXITY, LEARNING_RATE, EXAGGERATION)
    print("Reduced samples shape: {}".format(np.shape(reduced_samples)))
    # ########

    plot_clusters(reduced_samples, targets, "Keynote unbalanced actual", type = "actual")

    # Class balancing
    data = np.hstack((reduced_samples, np.reshape(targets, (len(targets), 1))))
    data, names = preprocessing.balance_classes(data, names, np.shape(reduced_samples)[1])
    print("Balanced data shape: {}".format(np.shape(data)))
    reduced_samples = data[:, :-1]
    targets = data[:, -1]
    # ###########


    plot_clusters(reduced_samples, targets, "Keynote balanced actual", type = "actual")
    
    # KMeans fit
    if(False):
        kmeans = KMeans(n_clusters = 3)

        print("Kmeans fitting")
        kmeans.fit(reduced_samples)
        predictions = kmeans.labels_

        print("Predictions shape: {}".format(np.shape(predictions)))

        plot_clusters(reduced_samples, predictions, "KMeans Keynote unsupervised", type = "predicted")

    # AgglomerativeClustering
    if(False):
        print()
        aggro = AgglomerativeClustering(n_clusters = 3)
        
        print("AgglomerativeClustering fitting")
        aggro.fit(reduced_samples)
        predictions = aggro.labels_

        plot_clusters(reduced_samples, predictions, "Agglomerative Clustering Keynote unsupervised", type = "predicted")

    # DBSCAN exploration
    if(False):
        print()
        for min_samples in np.arange(20, 50, 5):
            for eps in np.arange(4, 10, .5):
                print("mins_samples : {}, eps: {}".format(min_samples, eps))
                dbscan = DBSCAN(eps = eps, min_samples = min_samples)
                print("DBSCAN fitting")
                dbscan.fit(reduced_samples)

                predictions = dbscan.labels_
                
                print("Predictions shape: {}".format(np.shape(predictions)))
                unique, counts = np.unique(predictions, return_counts = True)
                print("The predictions are broken down as: {}".format(dict(zip(unique, counts))))
                # plot_clusters(reduced_samples, predictions, "DBSCAN Keynote unsupervised", type = "predicted")

                for i, prediction in enumerate(predictions):
                    if prediction == -1:
                        predictions[i] = unique[-1] + 1
                
                clustered = [[] for _ in unique]
                for i in range(len(reduced_samples)):
                    clustered[int(predictions[i])].append(reduced_samples[i])

                # colors = [plt.cm.Spectral(c) for c in unique]
                labels = ["label_{}".format(i+1) for i in unique]

                for i, cluster in enumerate(clustered):
                    cluster = np.array(cluster)
                    plt.scatter(cluster[:, 0], cluster[:, 1], label = labels[i], cmap = "RdBu")

                plt.legend()
                plt.title("DBSCAN clustering for eps:{}, min_samples:{}".format(eps, min_samples))
                plt.show()
                print()


    # DBSCAN fit
    if (True):
        print()
        dbscan = DBSCAN(eps = 3.5, min_samples = 60)
        print("DBSCAN fitting")
        dbscan.fit(reduced_samples)

        predictions = dbscan.labels_
        
        print("Predictions shape: {}".format(np.shape(predictions)))
        unique, counts = np.unique(predictions, return_counts = True)
        print("The predictions are broken down as: {}".format(dict(zip(unique, counts))))

        for i, prediction in enumerate(predictions):
            if prediction == -1:
                predictions[i] = unique[-1] + 1

        plot_clusters(reduced_samples, predictions, "DBSCAN Keynote unsupervised", type = "predicted")
        extract_to_file(names, reduced_samples, predictions)
        # study_clusters(samples, reduced_samples, predictions)




if __name__ == "__main__":
    main()
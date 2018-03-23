from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
import numpy as np

import data_handling, os, datetime, preprocessing, path_manipulations, tSNE_IO, results_IO, plotter, logger

import matplotlib
from matplotlib import pyplot as plt

PERPLEXITY = 30
LEARNING_RATE = 500
EXAGGERATION = 84
VISUALLY_BEST = False

def fit_kmeans(reduced_samples):
    kmeans = KMeans(n_clusters = 3)

    print("Kmeans fitting")
    kmeans.fit(reduced_samples)
    predictions = kmeans.labels_

    return predictions

def fit_AgglomerativeClustering(reduced_samples):
    aggro = AgglomerativeClustering(n_clusters = 3)
    aggro.fit(reduced_samples)
    predictions = aggro.labels_

    return predictions

def fit_DBSCAN(reduced_samples, eps, min_samples):
    dbscan = DBSCAN(eps = eps, min_samples = min_samples)
    dbscan.fit(reduced_samples)
    predictions = dbscan.labels_

    unique, counts = np.unique(predictions, return_counts = True)
    for i, prediction in enumerate(predictions):
        if prediction == -1:
            predictions[i] = unique[-1] + 1

    return predictions

def create_log_entry(conversation, eps, min_samples, tsne_params):
    entry = {
        "conversation" : "-".join(conversation),
        "perplexity" : tsne_params["perplexity"],
        "learning_rate" : tsne_params["learning_rate"],
        "early_exaggeration" : tsne_params["early_exaggeration"],
        "visually_best" : tsne_params["visually_best"],
        "eps" : eps,
        "min_samples" : min_samples
    }

    logger.store_log_entry(entry, "best_clustering_parameters_log.json")


def main():
    conversation = ["B", "A"]
    # conversation = []
    names = data_handling.read_names(["geco", data_handling.get_conversation_directory(conversation)])
    samples, _, zero_length_indices = data_handling.dataset(names)
    names = np.delete(names, zero_length_indices)
    speakers = data_handling.get_speakers(names)

    print("Original shapes, samples: {} \t names : {} \t speakers : {}".format(np.shape(samples), np.shape(names), np.shape(speakers)))
    
    # Samples Preprocessing
    samples = preprocessing.scale_select(samples)
    print("After feature selection shapes, samples: {}".format(np.shape(samples)))
    # ###########

    # Reduction
    print("Reduction")
    reduced_samples, tsne_params = tSNE_IO.load_or_reduce(samples, PERPLEXITY, LEARNING_RATE, EXAGGERATION, visually_best=VISUALLY_BEST)
    print("After dimensionality reduction shapes, samples: {}".format(np.shape(reduced_samples)))
    # ########

    
    if(True):
        # KMeans fit
        print()
        predictions = fit_kmeans(reduced_samples)
        plotter.plot_clusters(reduced_samples, predictions, "KMeans GECO unsupervised", speakers, VISUALLY_BEST)
        results_IO.clusters_to_file(names, reduced_samples, predictions, "KMeans", VISUALLY_BEST)

        # AgglomerativeClustering
        print()
        predictions = fit_AgglomerativeClustering(reduced_samples)
        plotter.plot_clusters(reduced_samples, predictions, "Agglomerative Clustering GECO unsupervised", speakers, VISUALLY_BEST)
        results_IO.clusters_to_file(names, reduced_samples, predictions, "Agglomerative_Clustering", VISUALLY_BEST)

        # DBSCAN fit
        # 3.1 35
        print()
        EPS = 2.8
        MIN_SAMPLES = 50
        predictions = fit_DBSCAN(reduced_samples, eps = EPS, min_samples = MIN_SAMPLES)
        
        unique, counts = np.unique(predictions, return_counts = True)
        print("The predictions are broken down as: {}".format(dict(zip(unique, counts))))

        create_log_entry(conversation, EPS, MIN_SAMPLES, tsne_params)
        plotter.plot_clusters(reduced_samples, predictions, "DBSCAN GECO unsupervised", speakers, VISUALLY_BEST)
        results_IO.clusters_to_file(names, reduced_samples, predictions, "DBSCAN", VISUALLY_BEST)

    # DBSCAN exploration
    if(False):
        print()
        for min_samples in np.arange(45, 60, 3):
            for eps in np.arange(2.6, 3.5, .05):
                print("mins_samples : {}, eps: {}".format(min_samples, eps))
                dbscan = DBSCAN(eps = eps, min_samples = min_samples)
                dbscan.fit(reduced_samples)

                predictions = dbscan.labels_
                
                print("Predictions shape: {}".format(np.shape(predictions)))
                unique, counts = np.unique(predictions, return_counts = True)
                print("The predictions are broken down as: {}".format(dict(zip(unique, counts))))
                # plotter.plot_clusters(reduced_samples, predictions, "DBSCAN Keynote unsupervised", type = "predicted")

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
                    plt.scatter(cluster[:, 0], cluster[:, 1], label = labels[i], cmap = "RdBu", marker = ".", linewidths = 0)

                plt.legend()
                plt.title("DBSCAN clustering for eps:{}, min_samples:{}".format(eps, min_samples))
                plt.show()
                print()




if __name__ == "__main__":
    main()
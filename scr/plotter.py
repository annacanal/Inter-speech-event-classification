import matplotlib
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
import data_handling, os, datetime, preprocessing, path_manipulations, warnings

def plot_clusters(samples, targets, dataset, speakers, visually_best):
    clustered = [[] for _ in np.unique(targets)]

    for i in range(len(samples)):
        clustered[int(targets[i])].append(i)

    cmap = plt.get_cmap("Dark2")

    # Different clustering process, based on number of clusters
    # If number of clusters > 3 assume DBSCAN and deal with method's noise
    if len(clustered) > 3:
        for i in range(len(clustered[:-1])):
            cluster = clustered[i]
            speaker_clusters = _get_speaker_clusters(cluster, speakers, samples)

            current_plot = _create_cluster_by_speakers(speaker_clusters, i, cmap)

        # Cluster for the DBSCAN noise
        cluster = clustered[-1]
        speaker_clusters = _get_speaker_clusters(cluster, speakers, samples)
        current_plot = _create_noise_cluster(speaker_clusters, current_plot)
    else:
        for i in range(len(clustered)):
            cluster = clustered[i]
            speaker_clusters = _get_speaker_clusters(cluster, speakers, samples)

            current_plot = _create_cluster_by_speakers(speaker_clusters, i, cmap)


    plt.legend()
    
    title = "{} - {} clusters".format(data_handling.conversation_directory.split("_")[1], dataset)
    plt.title(title)

    if visually_best:
        output_filename = "{}_visually_best_clusters.png".format("_".join(dataset.split()))
    else:
        output_filename = "{}_least_error_clusters.png".format("_".join(dataset.split()))

    output_dir = path_manipulations.create_or_return([data_handling.results_root, data_handling.conversation_directory, "img","unsupervised"])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, output_filename), dpi = 200)

    plt.show()

def _get_speaker_clusters(cluster, speakers, samples):
    speaker_clusters = [[] for _ in np.unique(speakers)]

    for sample_index in cluster:
        speaker_clusters[speakers[sample_index]].append(samples[sample_index, :])

    speaker_clusters = [np.array(c) for c in speaker_clusters]

    return speaker_clusters

def _create_cluster_by_speakers(speaker_clusters, i, cmap):
    color = cmap(i)
    if len(speaker_clusters[0]) > 1:
        plt.scatter(speaker_clusters[0][:, 0], speaker_clusters[0][:, 1], 
        facecolors='none', edgecolors = color, s=10, alpha = 1., marker = "o", 
        label = "cluster_{}".format(i), linewidths = .7)
    else:
        _cluster_of_one_speaker_warning("o")

    if len(speaker_clusters[1]) > 1:
        plt.scatter(speaker_clusters[1][:, 0], speaker_clusters[1][:, 1], 
        facecolors='none', edgecolors = color, s=10, alpha = 1., marker = "^", 
        linewidths = .7)
    else:
        _cluster_of_one_speaker_warning("^")

    return plt

def _create_noise_cluster(speaker_clusters, current_plot):
    color = "grey"
    current_plot.scatter(speaker_clusters[0][:, 0], speaker_clusters[0][:, 1], 
    facecolors='none', edgecolors = color, s=10, alpha = 0.5, marker = ".", 
    label = "DBSCAN Noise", linewidths = .7)

    current_plot.scatter(speaker_clusters[1][:, 0], speaker_clusters[1][:, 1], 
    facecolors='none', edgecolors = color, s=10, alpha = 0.5, marker = ".", 
    linewidths = .7)

    return current_plot

def _cluster_of_one_speaker_warning(speaker):
    warnings.warn("Cluster of only one speaker. Speaker: {}".format(speaker))
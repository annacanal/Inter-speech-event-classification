from sklearn import manifold

import numpy as np
import data_handling, os, preprocessing, path_manipulations, logger, time

import matplotlib
from matplotlib import pyplot as plt


def scatter_2D(reduced_samples, tsne_inst):
    plt.figure(1)
    plt.clf()
    plt.scatter(reduced_samples[:, 0], reduced_samples[:, 1], marker = '.', color = "black", linewidths = 0)

    tsne_params = tsne_inst.get_params()
    p = tsne_params["perplexity"]
    l_r = tsne_params["learning_rate"]
    ex = tsne_params["early_exaggeration"]
    features = data_handling.get_feature_set_size()

    # Make this store in different directories for different convos
    plt.title("tsne_reduced_dimensionality. {}f, {}p, {}lr, {}ex".format(features, p, l_r, ex))

    output_filename = "tsne_reduced_{}_{}_{}_{}.png".format(features, p, l_r, ex)
    output_dir = path_manipulations.create_or_return([data_handling.results_root, data_handling.conversation_directory, "img", "tsne_viz"])
    plt.savefig(os.path.join(output_dir,output_filename))
    
    # plt.show()


def cluster_scatter_2D(samples, targets, tsne_inst):
    plt.clf()
    clustered = [[] for _ in np.unique(targets)]

    for i in range(len(samples)):
        clustered[int(targets[i])].append(samples[i])

    labels = ["silences", "clicks", "breathing"]
    markers = [".", "*", "+"]

    for i, cluster in enumerate(clustered):
        cluster = np.array(cluster)
        plt.scatter(cluster[:, 0], cluster[:, 1], cmap = "RdBu", marker = markers[i], label = labels[i])

    tsne_params = tsne_inst.get_params()
    p = tsne_params["perplexity"]
    l_r = tsne_params["learning_rate"]
    ex = tsne_params["early_exaggeration"]
    features = data_handling.get_feature_set_size()

    plt.legend()
    plt.title("tsne_reduced_clusters. {}f, {}p, {}lr, {}ex".format(features, p, l_r, ex))

    output_filename = "clusters_tsne_reduced_{}_{}_{}_{}.png".format(features, p, l_r, ex)
    output_dir = path_manipulations.create_or_return([data_handling.results_root, data_handling.conversation_directory, "img", "tsne_viz"])
    plt.savefig(os.path.join( output_dir, output_filename))
    plt.show()

def main():
    # conversations = [("B", "A"), ("B", "M"), ("C", "E"), ("C", "F"), ("D", "G"), ("D", "L"), ("E", "I")]
    # conversations = [("E", "J"), ("F", "E"), ("F", "J"), ("G", "B"), ("G", "L")]
    conversations = [[]]
    for convo in conversations:
        convo_reduction_start = time.time()
        # names= data_handling.read_names(["case_study"])
        print("Conversation: ", convo)
        names = data_handling.read_names(["geco", data_handling.get_conversation_directory(convo)])
        samples, targets, zero_length_indices = data_handling.dataset(names)
        names = np.delete(names, zero_length_indices)

        print("original shapes, samples: {} \ttargets: {} \tnames: {}".format(np.shape(samples), np.shape(targets), np.shape(names)))
        samples = preprocessing.scale_select(samples)

        # data = np.hstack((samples, np.reshape(targets, (len(targets), 1))))
        # print("Data shape: {}".format(np.shape(data)))
        # unique, counts = np.unique(targets, return_counts = True)
        # print("Class breakdown: {}".format(dict(zip(unique, counts))))

        # data = preprocessing.balance_classes(data)
        # print("Balanced data shape: {}".format(np.shape(data)))
        # samples = data[:, :-1]
        # targets = data[:, -1]

        if(True):
            perplexities = [30]
            learning_rates = np.arange(300, 700, 100)
            # learning_rates = [200]
            exaggerations = [72, 84, 96]
            for perplexity in perplexities:
                for exaggeration in exaggerations:
                    for l_r in learning_rates:
                        print("p: {}, lr:{}, exag: {}".format(perplexity, l_r, exaggeration))
                        start = time.time()
                        # tsne = manifold.TSNE(n_components = 2, init='pca', perplexity=perplexity, early_exaggeration = exaggeration, 
                        #                     learning_rate = l_r, n_iter = 1000,
                        #                     random_state=data_handling.RANDOM_SEED, verbose = 1)

                        # reduced_samples = tsne.fit_transform(samples)

                        reduced_samples, tsne = preprocessing.tsne_reduction(samples, perplexity, l_r = l_r, ex = exaggeration,
                                                iterations=1000, verbosity=1)

                        end = time.time()
                        log_entry = {
                            "perplexity" : perplexity,
                            "learning_rate" : int(l_r),
                            "early_exaggeration" : int(exaggeration),
                            "final_error" : str(tsne.kl_divergence_)
                        }
                        logger.store_log_entry(log_entry, "tSNE_viz_log.json")

                        print("reduced samples shape: ", np.shape(reduced_samples))
                        print("Reduction took: {}\n".format(end-start))
                        # cluster_scatter_2D(reduced_samples, targets, tsne)
                        scatter_2D(reduced_samples, tsne)

                        print()
        convo_reduction_end = time.time()
        print("Conversation explored in: {}\n".format(convo_reduction_end-convo_reduction_start))
        
        if(False):
            tsne = manifold.TSNE(n_components = 2, init='pca', perplexity=5, early_exaggeration = 36, 
                                        learning_rate = 800, n_iter = 5000,
                                        random_state=data_handling.RANDOM_SEED, verbose = 1)

            reduced_samples = tsne.fit_transform(samples)


            log_entry = {
                "perplexity" : perplexity,
                "learning_rate" : l_r,
                "early_exaggeration" : exaggeration,
                "final_error" : tsne.kl_divergence_
            }
            logger.store_log_entry(log_entry, "tSNE_viz_log.json")

            print("reduced samples shape: ", np.shape(reduced_samples))
            cluster_scatter_2D(reduced_samples, targets, tsne)

            print()


if __name__ == "__main__":
    main()

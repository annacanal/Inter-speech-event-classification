import numpy as np
import path_manipulations, data_handling, os

def clusters_to_file(names, samples, targets, algo, visually_best):
    if np.shape(names)[0] != np.shape(samples)[0]:
        raise ValueError("length of names not equal to length of samples")

    if visually_best:
        output_filename = "{}_visually_best_clustering_out.csv".format(algo)
    else:
        output_filename = "{}_least_error_clustering_out.csv".format(algo)

    output_dir = path_manipulations.create_or_return([data_handling.results_root, data_handling.conversation_directory, "output_files"])
    with open(os.path.join(output_dir, output_filename), 'w') as f:
        for i, sample in enumerate(samples):
            # mono.A-C.left_1.680000_3.720000_25ms001.csv
            sample_name = names[i]

            # make sure that name is not part of a path (dealing with the all convos case)
            head, tail = os.path.split(sample_name)
            sample_name = tail

            parts = sample_name.split('_')
            start = parts[1]
            end = parts[2]
            sample_label = targets[i]

            line = "{}, {}, {}, {}, {}\n".format(i, sample_name, start, end, sample_label)
            f.write(line)

    print("Output file created in ", os.path.join(output_dir, output_filename))


def output_GECO_files_labels(names, labels):
    with open(os.path.join(results_root, conversation_directory, "output_files", "timestamps_and_clusters.csv"), "w") as f:
        for i, name in enumerate(names):
            cols = name.split('_')
            start = cols[1]
            end = cols[2][:-4]
            other_identifiers = cols[0].split('.')
            label = labels[i]

            line = "{}, {}, {}, {}, {}\n".format(i, name, start, end, label)
            f.write(line)

def dump_file(data, filename):
    with open(os.path.join(data_root, filename), 'w') as f:
        for datum in data:
            f.write("{}\n".format(datum))
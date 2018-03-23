import os, data_handling, path_manipulations, preprocessing, logger, operator
import numpy as np

PERPLEXITY = 30
LEARNING_RATE = 200
EXAGGERATION = 12
VISUALLY_BEST = True

LOG_NAME = "tSNE_viz_log.json"

def _save_reduced_samples(samples, filename = None):
    output_dir = _get_path_to_reductions()
    if filename is None:
        output_filename = "tsne_reduced_samples_{}_{}_{}.npy".format(PERPLEXITY, LEARNING_RATE, EXAGGERATION)
    else:
        output_filename = filename

    filename = os.path.join(output_dir, output_filename)

    np.save(filename, samples)
    print("\tFile with reduced data saved in ", filename)

def load_or_reduce(samples, p, l_r, ex, visually_best = True):
    _set_parameter_decision(visually_best)

    if visually_best:
        _set_globals(p, l_r, ex)
        reduced_samples = _best_visual_reduction(samples)
        _log_current_parameters()
    else:
        reduced_samples = _least_error_reduction(samples)

    return reduced_samples, _get_current_parameters()

def _best_visual_reduction(samples):
    dir = _get_path_to_reductions()
    filename = os.path.join(dir, "tsne_reduced_samples_{}_{}_{}.npy".format(PERPLEXITY, LEARNING_RATE, EXAGGERATION))

    reduced_samples = _get_reductions(samples, filename)

    return reduced_samples

def _least_error_reduction(samples):
    perplexity, learning_rate, exaggeration, error = _get_least_error_reduction_params()
    _set_globals(perplexity, learning_rate, exaggeration)

    dir = _get_path_to_reductions()
    filename = os.path.join(dir, "tsne_reduced_samples_{}_{}_{}.npy".format(PERPLEXITY, LEARNING_RATE, EXAGGERATION))

    reduced_samples = _get_reductions(samples, filename)

    return reduced_samples

def _get_reductions(samples, filename):
    if os.path.isfile(filename):
        print("\tFile with previous reduction found {}. Loading".format(filename))
        reduced_samples = np.load(filename)
    else:
        print("\tNo previous reductions found. Creating")
        reduced_samples, _ = preprocessing.tsne_reduction(samples, PERPLEXITY, l_r = LEARNING_RATE, ex = EXAGGERATION)

        _save_reduced_samples(reduced_samples)

    return reduced_samples

def _log_current_parameters():
    entry = _get_parameter_entry()

    logger.store_log_entry(entry, "tSNE_best_visually_log.json")

def _get_current_parameters():
    return _get_parameter_entry()

def _get_parameter_entry():
    entry = {
        "perplexity" : PERPLEXITY,
        "learning_rate" : LEARNING_RATE,
        "early_exaggeration" : EXAGGERATION,
        "visually_best" : VISUALLY_BEST
    }

    return entry

def _get_least_error_reduction_params():
    log_feed = logger.read_log(LOG_NAME)

    indexed_errors = {}
    for i, entry in enumerate(log_feed):
        indexed_errors[i] = float(entry["final_error"])

    ordered_indexed_error = sorted(indexed_errors.items(), key=operator.itemgetter(1))

    index_of_least_error_entry = ordered_indexed_error[0][0]
    least_error_entry = log_feed[index_of_least_error_entry]

    return _parameters_from_entry(least_error_entry)


def _parameters_from_entry(entry):
    perplexity = entry["perplexity"]
    learning_rate = entry["learning_rate"]
    early_exaggeration = entry["early_exaggeration"]
    error = float(entry["final_error"])

    return perplexity, learning_rate, early_exaggeration, error

def _get_path_to_reductions():
    return path_manipulations.create_or_return([data_handling.results_root, data_handling.conversation_directory, "tSNE_reduced_files"])



def _set_globals(p, l_r, ex):
    global PERPLEXITY
    PERPLEXITY = p

    global LEARNING_RATE
    LEARNING_RATE = l_r

    global EXAGGERATION
    EXAGGERATION = ex

def _set_parameter_decision(visually_best):
    global VISUALLY_BEST
    VISUALLY_BEST = visually_best
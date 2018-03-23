

import numpy as np
import csv, os, operator, warnings, path_manipulations

RANDOM_SEED = 1337
np.random.seed(RANDOM_SEED)

FEATURES = 338

data_root = "../data"
dataset_root = "../data"
results_root = "../results"

conversation_directory = "."

def set_data_root(from_here):
    if type(from_here) is not list:
        from_here = [from_here]
    
    global data_root
    data_root = os.path.join("../data", from_here[0])

    global dataset_root
    dataset_root = os.path.join("../data", from_here[0])

    global results_root
    results_root = os.path.join("../results", from_here[0])

    for subpath in from_here[1:]:
        data_root = path_manipulations.create_or_return([data_root, subpath])

def targets_exist():
    if current_database_is_("keynote"):
        return True

    return False

def current_database_is_(database):
    if data_root.find(database) is not -1:
        return True

    return False

def get_feature_set_size():
    return FEATURES

def read_names(from_here):
    set_data_root(from_here)

    with open(os.path.join(data_root,"list.txt"), "r") as f:
        # Read the whole file at once
        names = f.readlines()
    names = [x.strip() for x in names]
    return names

def get_speakers(names):
    if not current_database_is_("geco"):
        raise ValueError("Speakers are only relevant in the GECO database")
    else:
        speakers = []
        for name in names:
            # make sure that name is not part of a path (dealing with the all convos case)
            head, tail = os.path.split(name)
            name = tail
            
            parts = name.split('_')
            speaker_part = parts[0].split('.')
            speaker = speaker_part[-1]

            if speaker == "left":
                speaker = 0
            elif speaker == "right":
                speaker = 1
            else:
                raise ValueError("More than two speakers?")
            
            speakers.append(speaker)

        return speakers


def dataset(names):
    samples_dim = len(names)
    features_dim = get_feature_set_size()

    train = []
    targets = []

    zero_length_features = 0
    zl_indices = []
    for i in range(len(names)):
        features = extract_features(names[i])
        
        if len(features) < features_dim:
            zl_indices.append(i)
            zero_length_features += 1
            continue
        else:
            if targets_exist():
                target = get_class(names[i])
                targets.append(target)
            

            train.append([float(feature) for feature in features])

    print("{} samples with no features".format(zero_length_features))

    return np.array(train), np.array(targets), zl_indices


def extract_features(file_name):
    with open(os.path.join(data_root, file_name)) as csvfile:
        reader = csv.reader(csvfile, delimiter='@', quotechar='|')
        data = []
        for row in reader:  # Number of rows
            data.append(row)
    features1 = data[len(data) - 1]
    features1=str(features1)
    features= [feat for feat in features1.split(',')]
    features[0] = '0'
    features[len(features)-1] = '0'
    return features


def get_class(filename):
    cols = filename.split('_')
    target = cols[3]

    return class_to_numerical(target)

def class_to_numerical(target):
    if target == "silences":
        return 0
    elif target == "clicks":
        return 1
    elif target == "breathing":
        return 2
    else:
        raise ValueError("Unexpected target value: {}".format(target))


def get_conversation_directory(list_people):
    if type(list_people) is not list or len(list_people) > 2 or len(list_people) == 1:
        raise ValueError("Please provide a list of two letters, corresponding to the speakers, or the string \"list.txt\" ")

    if len(list_people) == 0:
        warnings.warn("Assuming you are attempting to process all conversations")

        dir_name = "."
        global conversation_directory
        conversation_directory = "all_conversations"

        return dir_name
    else:
        speaker_1 = list_people[0].upper()
        speaker_2 = list_people[1].upper()
        dir_name = "25ms_{}-{}".format(speaker_1, speaker_2)

        # global conversation_directory
        conversation_directory = dir_name

        return dir_name


if __name__ == "__main__":
    main()

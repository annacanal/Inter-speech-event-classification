import data_handling, path_manipulations
import json, os

def store_log_entry(entry, file = "log.json"):
    output_dir = path_manipulations.create_or_return([data_handling.results_root, data_handling.conversation_directory, "logs"])
    log = os.path.join(output_dir, file)

    if not os.path.isfile(log):
        with open(log, "w") as f:
            log_feed = []
            json_p = json.dumps(log_feed)
            f.write(json_p)
    
    with open(log, "r") as f:
        log_feed = json.load(f)
        log_feed.append(entry)

    with open(log, "w") as f:
        json_p = json.dumps(log_feed, indent = 3)
        f.write(json_p)

def read_log(log_name):
    log_path = get_path_to_log(log_name)

    with open(log_path, 'r') as f:
        log_feed = json.load(f)

    return log_feed


def get_path_to_log(log_name):
    return path_manipulations.return_path([data_handling.results_root, data_handling.conversation_directory, "logs", log_name])
import os, data_handling, warnings


# Accepts path components as a list,
# and returns a full path after
# ensuring its existance. If the path
# does not exist, it creates it
def create_or_return(path_components):
    if type(path_components) is not list:
        path_components = [path_components]

    output_dir = "."
    for dir in path_components:
        output_dir = os.path.join(output_dir, dir)

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        
    return output_dir

def return_path(path_components):
    if type(path_components) is not list:
        path_components = [path_components]

    path = "."
    for path_part in path_components:
        path = os.path.join(path, path_part)

    return path
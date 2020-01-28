import os
from typing import List, Tuple

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from scipy.io import loadmat

import utils

S3_URL = 'https://bea-portfolio.s3-us-west-2.amazonaws.com/feature-reduction/'
COLOR1 = '#3F4F8C'


def load_data(cam_index: int) -> List[np.ndarray]:
    """
    Creates a 'data' folder if it doesn't exist and loads data for this project 
    if it's not yet present in the 'data' folder. Returns the loaded data.
    """

    # Download mat files from Amazon S3 if they're not yet local.
    index_list = [1, 2, 3]
    filenames = [f'cam{cam_index}_{j}.mat' for j in index_list]
    local_paths = []
    for filename in filenames:
        remote_url = S3_URL + filename
        local_path = utils.download_remote_data_file(remote_url)
        local_paths.append(local_path)

    # Load each data file into memory.
    data_files = [loadmat(local_path, struct_as_record=False) for local_path 
        in local_paths]
    
    # Extract information for each data files into an array.
    # Each arrary is of size 480 x 640 x 3 x 226. This corresponds to 226 
    # color images, of size 480 x 640.
    data_list = [data_files[j-1][f'vidFrames{cam_index}_{j}'] for j in index_list]

    return data_list


def main() -> None:
    """
    Main program.
    """
    
    print('Main')
    plots_dir_path = utils.find_or_create_plots()
    load_data(1)


if __name__ == '__main__':
    main()

"""
Author: Kartikey Sinha
"""

#####
# Import important libraries
#####

import pandas as pd
import requests
import zipfile
import os
from typing import List
import shutil


#####
# Define variables
#####

DATA_DIR = "./data/"

# List of all files we get from unzipping
all_files = ['NONDERIV_TRANS.tsv',
 'NONDERIV_HOLDING.tsv',
 'OWNER_SIGNATURE.tsv',
 'REPORTINGOWNER.tsv',
 'DERIV_HOLDING.tsv',
 'insider_transactions_metadata.json',
 'insider_transactions_readme.htm',
 'DERIV_TRANS.tsv',
 'SUBMISSION.tsv',
 'FOOTNOTES.tsv'
]

interested_files = ['NONDERIV_TRANS.tsv', 'NONDERIV_HOLDING.tsv',]


#####
# Define helper functions
#####

def get_insider_data_quaterly(year: int, quarter: int, data_dir:str = DATA_DIR) -> str:
    """
    For the givem year and quarter, get the insider trading information as a zip file. Unzips that file in data_dir.
    Returns the folder name where the data is unzipped.
    """

    base_url = f'https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{str(year)}q{str(quarter)}_form345.zip'
    retval = requests.get(url=base_url)

    file_name = base_url.split('/')[-1]
    folder_name = file_name.split('.')[0]
    full_path = data_dir + file_name

    # Download the zip file in the data_dir
    with open(full_path, 'wb') as output_file:
        output_file.write(retval.content)
    
    # Create folder to extract files
    os.makedirs(os.path.join(data_dir, folder_name))
    
    try:
        # Extract the zip-files
        with zipfile.ZipFile(f'{full_path}', 'r') as zip_ref:
            zip_ref.extractall(os.path.join(data_dir, folder_name))
    except zipfile.BadZipFile as e:
        os.unlink(full_path)
        shutil.rmtree(os.path.join(data_dir, folder_name))
        print(f"data doesn't exist for {year} : {quarter}" )
        return ""
    
    return folder_name


def get_insider_data_from_files(interested_folders: List[str], interested_files: List[str] = all_files, data_dir:str = DATA_DIR) -> dict:
    """
    For the interested fodlers and files in the data_dir, read and aggregate all the data, and return it in the form of dictionary.
    Ex. interested_files = ['a', 'b']
        returned_dict = {'a': pd.DataFrame(all data in file 'a' in all files), 
                         'b': pd.DataFrame(all data in file 'a' in all files)}
    """

    d_data = {f:pd.DataFrame() for f in interested_files}

    for folder in interested_folders:
        for file in interested_files:
            if os.path.isfile(data_dir + folder + "/" + file):
                tmp_df = pd.read_csv(data_dir + folder + "/" + file, sep='\t', low_memory=False)
                d_data[file] = pd.concat([d_data[file], tmp_df])

    return d_data


def cleanup(data_dir:str = DATA_DIR) -> None:
    """
    Deleted all the files and fodlers that were created in the data collection process.
    """

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return


def run_data_collection(years:List[int], quarters:List[int], interested_files:List[str], data_dir:str = DATA_DIR) -> dict:
    """
    Runs the data collection process for the given years, quarters, and interested files.
    Returns a dictionary where the key is the interested file, and the value is the data aggregated for that file.

    Assumes that the data_dir exists.
    """

    lst_folders = []

    for year in years:
        for quar in quarters:
            lst_folders.append(get_insider_data_quaterly(year=year, quarter=quar, data_dir=data_dir))

    data_dict = get_insider_data_from_files(interested_files=interested_files, interested_folders=lst_folders, data_dir=data_dir)

    cleanup(data_dir=data_dir)

    return data_dict

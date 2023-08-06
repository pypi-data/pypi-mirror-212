import os
import datetime
import pickle
import time
from logging.config import fileConfig
import logging
from pdb import set_trace as bp



def file_last_update_datetime(filepath:str, datetime_only:bool=False):
    modTimesinceEpoc = os.path.getmtime(filepath)
    modificationTime = datetime.datetime.utcfromtimestamp(modTimesinceEpoc).strftime('%Y-%m-%d %H:%M')
    if datetime_only:
        return modificationTime
    else:
        return 'Last Update: \n' + modificationTime + ' UTC'


def all_dict_values_in_target_types(
    input_dict: dict,
    target_types: list,
    visible_key_only = True
) -> bool:
    """check if all values of input dictionary are in target types

    Args:
        input_dict (dict): dictionary wait to check
        target_types (list): list of types
        visible_key_only (bool, optional): only check dictionary keys not starting from underscore. Defaults to True.

    Returns:
        bool : True or False
    """
    if visible_key_only:
        return all(type(v) in target_types for k,v in input_dict.items() if not k.startswith('_'))
    else:
        return all(type(v) in target_types for k,v in input_dict.items())
    


def from_cache_if_possible(df_name:str, cache_dir:str, refresh_func:callable,**kwarg):
    """provide basic functionality to load pickle file as a variable if it exists; otherwise, call refresh_func to return the data

    Args:
        df_name (str): variable name
        cache_dir (str): path for checking the existance of pickle file
        refresh_func (callable): function to return the intended data

    Returns:
        obj: instance of intended data
    """
    cache_path=os.path.join(
        cache_dir,
        f"{df_name}.pkl"
    )
    if os.path.exists(cache_path):
        file = open(cache_path, 'rb')
        df = pickle.load(file)
        file.close()
        #df = pd.read_pickle(cache_path)
    else:
        df = refresh_func(**kwarg)
        file = open(cache_path, 'wb')
        pickle.dump(df, file)
        file.close()
        #pd.to_pickle(df, cache_path)
    return df

#not yet ready for releasing, need testing
def start_logging():

    if not os.path.exists('log'): os.mkdir('log')

    time_tag = time.strftime("%Y%m%d_%H%M%S")
    log_file_name = f'log/{time_tag}.log'

    fileConfig(
        'logging.ini',
        defaults={'log_file_name': log_file_name},
        disable_existing_loggers=False
    )

    logger = logging.getLogger(__name__)
    logger.info(f'Toybox has been opened')
    return logger
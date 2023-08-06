import pickle
from sys import getsizeof


def easy_dump(obj, file_name):
    if not file_name.endswith('.pkl'):
        file_name += '.pkl'
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)


def easy_load(file_name: str):
    if not file_name.endswith('.pkl'):
        file_name += '.pkl'
    with open(file_name, 'rb') as f:
        obj = pickle.load(f)
        print('object type:', type(obj))
        print('object size: ', getsizeof(obj))
        return obj

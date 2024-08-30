import pickle 
import joblib
import os


def get_input_features_from_file(path) -> list[str]: 
    extension = os.path.splitext(os.path.basename(path))[1]
    if extension == ".pkl":
        return get_features_pkl(path)
    elif extension == ".joblib":
        ...
    else: 
        print("Can't retrieve input features names from this type of file")



def get_features_pkl(path) -> list[str]:
    with open(path, "rb") as f:
        model = pickle.load(f)

    try:
        input_features = model.feature_names_in_
    except AttributeError:
        input_features = []
        print("Model does not store input feature names.")
    
    return input_features


def get_features_joblib(path) -> list[str]:
    with open(path, "rb") as f:
        model = joblib.load(f)

    try:
        input_features = model.feature_names_in_
    except AttributeError:
        input_features = []
        print("Model does not store input feature names.")
    
    return input_features
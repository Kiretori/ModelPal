import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
import pickle
import joblib
import os


def get_input_features_from_file(path) -> list[str]:
    extension = os.path.splitext(os.path.basename(path))[1]
    if extension == ".pkl":
        return _get_features_pkl(path)
    elif extension == ".joblib":
        return _get_features_joblib(path)
    else:
        print("Can't retrieve input features names from this type of file")
        return list()


def _get_features_pkl(path) -> list[str]:
    with open(path, "rb") as f:
        model = pickle.load(f)

    try:
        input_features = model.feature_names_in_
    except AttributeError:
        input_features = []
        print("Model does not store input feature names.")

    return input_features


def _get_features_joblib(path) -> list[str]:
    with open(path, "rb") as f:
        model = joblib.load(f)

    try:
        input_features = model.feature_names_in_
    except AttributeError:
        input_features = []
        print("Model does not store input feature names.")

    return input_features


def get_predictions(input_features: list[str], model: BaseEstimator, data: np.ndarray | pd.DataFrame):
    corrected_data = data[input_features]
    predictions = model.predict(corrected_data)
    return predictions

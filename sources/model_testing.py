import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sources.modelling import Model


def show_accuracy():
    accuracy= Model.get_accuracy()
    return accuracy


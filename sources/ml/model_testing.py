
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from .modelling.modelling import Model
from ..data_pipeline.data_pipeline import global_transformer, next_events, history

#récupération du modèle de ML de modelling.py
mon_model= Model()
mon_model.modelling()

#définition de la variable weekly_accuracy qui sera l'accuracy calculer chaque semaine après avoir rechargé les données de l'API
weekly_accuracy=mon_model.get_accuracy()
#print(weekly_accuracy)

# copie dans accuracy.txt
with open("accuracy.txt", "w") as f:
    f.write(str(weekly_accuracy))
#dans git action, si l'accuracy est <0.6, une alerte est émise
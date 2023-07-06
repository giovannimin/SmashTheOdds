# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 17:09
@author: GiovanniMINGHELLI
"""

import re
import os
from datetime import datetime, timedelta


def get_root(root: str = "SmashTheOdds"):
    """
    Renvoie le chemin racine du projet spécifié.
    :param root: (str) Nom de la racine du projet.
    :return: (str) Chemin racine du projet.
    """
    proj_path = os.getcwd()
    while os.path.basename(proj_path) != root:
        proj_path = os.path.dirname(proj_path)
        os.chdir(proj_path)
    return proj_path


def get_number_in_id(sr_id: str) -> str:
    """
    Les identifiants sont encodés dans l'API Tennis sous la forme (sr:competitor:983784, sr:tournament:87389, etc.)
    Renvoie l'identifiant sans le préfixe.
    :param sr_id: (str) Identifiant encodé.
    :return: (str) Identifiant sans préfixe.
    """
    numbers = re.findall(r'\d+', sr_id)
    return int(numbers[0]) if numbers else ""


def check_file_modification(file_path, since: int = 3):
    """
    Vérifie si un fichier a été modifié au cours des "since" derniers jours.
    :param file_path: (str) Chemin du fichier à vérifier.
    :param since: (int) Nombre de jours à prendre en compte pour la vérification (par défaut: 3).
    :return: (bool) True si le fichier a été modifié récemment, False sinon.
    """
    if os.path.isfile(file_path):
        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
        three_days_ago = datetime.now() - timedelta(days=since)
        if file_modified >= three_days_ago:
            return True
    return False


def calculate_odds(probability):
    """
    Calcule les cotes à partir d'une probabilité de victoire.

    :param probability: (float) Probabilité de victoire (entre 0 et 1).
    :return: (float) Cotes.
    """
    odds = 1 / probability
    return odds


def get_last_model():
    """
    Renvoi le chemin du dernier modèle modifié à la racine du projet
    :return: (str): chemin absolu du dernier modèle
    """
    last_model = sorted([file for file in os.listdir(get_root()) if file.startswith('model_')],
                        key=lambda x: os.path.getmtime(os.path.join(get_root(), x)), reverse=True)[0]
    return os.path.join(get_root(), last_model)



def get_response(model, data):
    results = {'classe': model.predict(data).tolist(), 'proba': model.predict_proba(data).round(2).tolist()}
    results['odds'] = calculate_odds(results['proba']).round(2)
    return results



#Fonction de gestion des id pré :
#Fonction de gestion des features :
#Fonctions des test ATP, Masculin, etc..
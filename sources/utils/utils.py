# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 17:09
@author: GiovanniMINGHELLI
"""

import os
import pandas as pd
import re
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


def replace_player_ids_with_rank(dataframe: pd.DataFrame, ranking: pd.DataFrame, unranked: int = 1000) -> pd.DataFrame:
    # Création d'un dictionnaire pour mapper les ID des joueurs avec les classements ATP
    player_rank_mapping = dict(zip(ranking['id'], ranking['rank']))
    # Modification des ID des joueurs par les classements ATP associés
    dataframe[['player1_rank', 'player2_rank']] = dataframe[['player1_id', 'player2_id']].replace(player_rank_mapping)
    # Remplacement des ID des joueurs hors classement ATP par 1000 pour marquer la différence
    dataframe['player1_rank'] = dataframe['player1_rank'].replace(to_replace='^.*$', value=unranked, regex=True)
    dataframe['player2_rank'] = dataframe['player2_rank'].replace(to_replace='^.*$', value=unranked, regex=True)
    return dataframe

def speed_feature_engineering(dataframe: pd.DataFrame, ranking: pd.DataFrame) -> pd.DataFrame:

    player_movement = dict(zip(ranking['id'], ranking['ranking_movement']))
    player_form = dict(zip(ranking['id'], ranking['ranking_movement'].apply(lambda x: -1 if x < 0 else 1 if x > 0 else 0)))
    player_atp_points = dict(zip(ranking['id'], ranking['points']))
    player_tournaments_played = dict(zip(ranking['id'], ranking['tournaments_played']))

    dataframe[['player1_ranking_movement', 'player2_ranking_movement']] = dataframe[['player1_id', 'player2_id']].replace(player_movement)
    dataframe[['player1_form', 'player2_form']] = dataframe[['player1_id', 'player2_id']].replace(player_form)
    dataframe[['player1_atp_points', 'player2_atp_points']] = dataframe[['player1_id', 'player2_id']].replace(player_atp_points)
    dataframe[['player1_tournaments_played', 'player2_tournaments_played']] = dataframe[['player1_id', 'player2_id']].replace(player_tournaments_played)

    return dataframe

def filter_dataframe(dataframe: pd.DataFrame, filters: dict):
    for column, values in filters.items():
        dataframe = dataframe[dataframe[column].isin(values)]
    return dataframe


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
    last_model = [file for file in os.listdir(get_root()) if file.startswith('model_')]
    if last_model:
        model_list = sorted(last_model, key=lambda x: os.path.getmtime(os.path.join(get_root(), x)), reverse=True)
        return os.path.join(get_root(), model_list[0])
    return None


def get_response(model, data):
    results = {'classe': int(model.predict(data)),
               'proba': model.predict_proba(data).round(2).flatten().tolist(),
               'odds': (calculate_odds(model.predict_proba(data))).round(2).flatten().tolist()}
    return results

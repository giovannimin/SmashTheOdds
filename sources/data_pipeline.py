# -*- coding: utf-8 -*-
"""
Created on 03/07/2023 15:06
@author: GiovanniMINGHELLI
"""
import os

import pandas as pd
import numpy as np
from .preprocessor import get_weekly_schedule, prep_ranking
from .utils import get_root, check_file_modification, replace_player_ids_with_rank, filter_dataframe


def history(df: pd.DataFrame() = pd.read_csv(os.path.join(get_root(), 'database.nosync', 'updated_table.csv'))):
    """
    Fonction pour traiter l'historique des matchs des joueurs classés ATP.
    :param df: (pd.DataFrame) DataFrame contenant les données des matchs.
    :return: (pd.DataFrame) DataFrame traité contenant les colonnes 'winner_is', 'player1_id' et 'player2_id'.
    """
    # Modification des ID joueurs par le classement ATP associé
    df = replace_player_ids_with_rank(dataframe=df, ranking=prep_ranking(), unranked=1000)

    # Création de la variable cible, 0 si le joueur 1 gagne et 1 si le joueur 2 gagne
    df['winner_is'] = np.where(df['player1_id'] == df['winner_id'], 0, 1)

    def inverse_dual(df_1: pd.DataFrame):
        """
        Fonction qui permet de dupliquer la table en inversant le joueur 1 et 2 pour retourner le problème
        :param df_1: (pd.DataFrame) DataFrame initial.
        :return: (pd.DataFrame) DataFrame inversé.
        """
        df2 = df_1.copy()
        df2['player1_id'], df2['player2_id'] = df_1['player2_id'], df_1['player1_id']
        df2['home_score'], df2['away_score'] = df_1['away_score'], df_1['home_score']
        df2['winner_is'] = df['winner_is'].replace({0: 1, 1: 0})
        return pd.concat([df_1, df2], axis=0)

    df = inverse_dual(df_1=df)
    df.drop_duplicates(inplace=True)
    return df[['winner_is', 'player1_id', 'player2_id']]


def next_events(df: str = os.path.join(get_root(), 'database.nosync', 'planning_table.csv')):
    """
    Fonction pour récupérer les prochains événements.
    :param df: (str) chemin du DataFrame contenant les données des prochains événements.
    :return: (pd.DataFrame) DataFrame des prochains événements traités.
    """
    # Verification de la dernière MAJ du planning, par défaut 3 jours
    if check_file_modification(df, since=3):
        planning = pd.read_csv(df)
    else:
        planning = get_weekly_schedule()

    # Modification des ID joueurs par le classement ATP associé
    planning = replace_player_ids_with_rank(dataframe=planning, ranking=prep_ranking(), unranked=1000)

    # Sélection uniquement des match ATP n'ayant pas encore commencés
    planning = filter_dataframe(dataframe=planning, filters={
        'tournament.category.name': ['ATP'],
        'status': ['match_about_to_start', 'not_started']
    })

    return planning[['player1_id', 'player2_id']]


def global_transformer(df: pd.DataFrame):
    # Modification des ID joueurs par le classement ATP associé
    df = replace_player_ids_with_rank(dataframe=df, ranking=prep_ranking(), unranked=1000)
    # Création de la variable rank_diff
    df.loc[:, 'atp_difference'] = df['player2_id'] - df['player1_id']
    # Gestion des affrontement hors ATP
    return df


if __name__ == "__main__":
    train_set = global_transformer(history())
    val_set = global_transformer(next_events())

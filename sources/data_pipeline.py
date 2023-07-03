# -*- coding: utf-8 -*-
"""
Created on 03/07/2023 15:06
@author: GiovanniMINGHELLI
"""
import os

import pandas as pd
import numpy as np
from sources.preprocessor import get_weekly_schedule
from sources.preprocessor import prep_ranking
from sources.utils import get_root


def history(df: pd.DataFrame() = pd.read_csv(os.path.join(get_root(), 'database.nosync', 'updated_table.csv'))):
    # Instantion d'une table ranking
    data = prep_ranking()
    # Modification des ID joueurs par le classement ATP associé
    df[['player1_id', 'player2_id', 'winner_id']] = df[['player1_id', 'player2_id', 'winner_id']].replace(
        dict(zip(data['id'], data['rank'])))
    # Remplacement des ID joueurs hors classement ATP par un 1000 pour marquer la différence
    df['player1_id'] = df['player1_id'].replace(to_replace='^.*$', value=1000, regex=True)
    df['player2_id'] = df['player2_id'].replace(to_replace='^.*$', value=1000, regex=True)
    # Création de la variable cible, 0 si le joueur 1 gagne et 1 si le joueur 2 gagne
    df['winner_is'] = np.where(df['player1_id'] == df['winner_id'], 0, 1)

    def inverse_dual(df_1: pd.DataFrame):
        df2 = df_1.copy()
        df2['player1_id'], df2['player2_id'] = df_1['player2_id'], df_1['player1_id']
        df2['home_score'], df2['away_score'] = df_1['away_score'], df_1['home_score']
        df2['winner_is'] = df['winner_is'].replace({0: 1, 1: 0})
        return pd.concat([df_1, df2], axis=0)

    df = inverse_dual(df_1=df)
    df.drop_duplicates(inplace=True)
    return df[['player1_id', 'player2_id']]


def next_events():
    planning = get_weekly_schedule()
    # Instantion d'une table ranking
    data = prep_ranking()
    # Modification des ID joueurs par le classement ATP associé
    planning[['player1_id', 'player2_id']] = planning[['player1_id', 'player2_id']].replace(
        dict(zip(data['id'], data['rank'])))
    # Remplacement des ID joueurs hors classement ATP par un 1000 pour marquer la différence
    planning['player1_id'] = planning['player1_id'].replace(to_replace='^.*$', value=1000, regex=True)
    planning['player2_id'] = planning['player2_id'].replace(to_replace='^.*$', value=1000, regex=True)
    return planning[['player1_id', 'player2_id']]


def global_transformer(df: pd.DataFrame):
    # Création de la variable rank_diff
    df['atp_difference'] = df['player1_id'] - df['player2_id']
    # Suppression des affrontement n'ayant pas au moins un des deux joueur classé ATP
    df = df[(df['player1_id'] != 1000) & (df['player2_id'] != 1000)]
    return df


if __name__ == "__main__":
    train_set = global_transformer(history())
    val_set = global_transformer(next_events())

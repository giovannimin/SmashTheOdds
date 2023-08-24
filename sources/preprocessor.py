# -*- coding: utf-8 -*-
"""
Created on 24/05/2023 22:07
@author: GiovanniMINGHELLI
"""
import os
from typing import List

import pandas as pd
from tqdm import tqdm
from datetime import date

from sources.get_data import Tennis
from sources.utils import get_number_in_id, check_file_modification, get_root
from sources.week_calendar import get_next_seven_days

today = date.today()


def prep_daily_results(year=today.year, month=today.month, day=today.day):
    return Tennis().get_daily_results(year=year, month=month, day=day)


def get_weekly_schedule():
    df_list = []
    for date in get_next_seven_days():
        year, month, day = map(int, date.split('-'))
        response = Tennis().get_daily_schedule(year=year, month=month, day=day)
        if response.status_code != 200:
            return response.json()
        df_response = pd.json_normalize(response.json()['sport_events'])
        df_response[['player1', 'player2']] = df_response['competitors'].apply(pd.Series)
        player1_df = pd.json_normalize(df_response['player1']).add_prefix('player1_') # type: ignore
        player2_df = pd.json_normalize(df_response['player2']).add_prefix('player2_') # type: ignore

        df = pd.concat([df_response, player1_df, player2_df], axis=1)
        df_list.append(df)
    return pd.concat(df_list, axis=0, ignore_index=True)


def get_match_info(match_id: int):
    response = Tennis().get_match_summary(match_id=match_id)
    if response.status_code != 200:
        return response.json()
    df_response = pd.json_normalize(response.json()['sport_event'])
    df_response[['player1', 'player2']] = df_response['competitors'].apply(pd.Series)
    player1_df = pd.json_normalize(df_response['player1']).add_prefix('player1_') # type: ignore
    player2_df = pd.json_normalize(df_response['player2']).add_prefix('player2_') # type: ignore
    df = pd.concat([df_response, player1_df, player2_df], axis=1)
    data = prep_ranking()
    df[['player1_id', 'player2_id']] = df[['player1_id', 'player2_id']].replace(dict(zip(data['id'], data['rank'])))
    return df


def get_match_proba(match_id: int) -> tuple:
    response = Tennis().get_match_proba(match_id=match_id)
    if response.status_code != 200:
        return response.json()
    home = response.json()['probabilities']['markets'][-1]['outcomes'][0]['probability']
    away = response.json()['probabilities']['markets'][-1]['outcomes'][1]['probability']
    return home, away


def prep_competition() -> pd.DataFrame:
    # Obtenir les données de compétition
    competition_data = Tennis().get_competition().json()['tournaments']
    # Créer le DataFrame initial en filtrant les colonnes indésirables
    data = pd.DataFrame(competition_data).drop(['sport', 'name'], axis=1)
    # Renommer la colonne 'id' en 'tournament_id'
    data = data.rename(columns={'id': 'tournament_id'})
    # Étendre le DataFrame avec les informations de la saison actuelle
    data = pd.concat([data, data['current_season'].apply(pd.Series)], axis=1).drop(['name', 'current_season'], axis=1)
    # Renommer la colonne 'id' en 'season_id'
    data = data.rename(columns={'id': 'season_id'})
    # Étendre le DataFrame avec les informations de la catégorie
    data = pd.concat([data, data['category'].apply(pd.Series)], axis=1).drop(['category'], axis=1)
    # Renommer la colonne 'id' en 'category_id'
    data = data.rename(columns={'id': 'category_id'})
    # Filtrer les lignes avec 'name' égal à 'ATP'
    data = data[data['name'] == 'ATP']
    return data


def prep_ranking() -> pd.DataFrame:
    # Verification de si le classement a moins de 72h
    if check_file_modification(os.path.join(get_root(), 'database.nosync', 'atp_ranking.csv'), since=3):
        return pd.read_csv(os.path.join(get_root(), 'database.nosync', 'atp_ranking.csv'))
    else:
        # Obtenir les données de classement
        ranking_data = pd.DataFrame(Tennis().get_ranking().json()['rankings'])
        # Filtrer les données pour la compétition 'ATP'
        data = pd.DataFrame(ranking_data.loc[ranking_data['name'] == 'ATP', 'player_rankings'].iloc[0])
        # Étendre le DataFrame avec les informations du joueur
        data = pd.concat([data, data['player'].apply(pd.Series)], axis=1)
        # Supprimer les colonnes indésirables
        data.drop(['player', 'name', 'nationality', 'country_code', 'abbreviation'], axis=1, inplace=True)
        # Actualisation du classement
        data.to_csv(os.path.join(get_root(), 'database.nosync', 'atp_ranking.csv'), index=False)
        return data


def prep_player(player_id: int) -> pd.DataFrame:
    # Récupération des résultats du joueur à partir de l'API
    data = pd.DataFrame(Tennis().get_player_result(player_id=player_id).json()['results'])
    # Extraction des json de la colonne 'sport_event' en tant que nouvelles colonnes
    data_1 = pd.concat([data, data['sport_event'].apply(pd.Series)], axis=1).drop('sport_event', axis=1)
    data_1 = data_1.rename(columns={'id': 'match_id'})
    # Extraction des json de la colonne 'competitors' en tant que nouvelles colonnes
    data_1 = pd.concat([data_1, data_1['competitors'].apply(pd.Series)], axis=1).drop('competitors', axis=1)
    # Extraction des colonnes '0' et '1' contenant les infos joueurs
    data_2 = pd.concat([data_1, data_1.iloc[:, -1].apply(pd.Series)], axis=1)
    data_2 = data_2.rename(columns={'id': 'player1_id'})
    data_2 = pd.concat([data_2, data_1.iloc[:, -2].apply(pd.Series)], axis=1)
    data_2 = data_2.rename(columns={'id': 'player2_id'})
    # Extraction des json de la colonne 'sport_event_status' en tant que nouvelles colonnes
    data_2 = pd.concat([data_2, data_2['sport_event_status'].apply(pd.Series)], axis=1).drop('sport_event_status',
                                                                                             axis=1)
    # Sélection des colonnes pertinentes pour le résultat final
    return data_2[['match_id', 'scheduled', 'player1_id', 'player2_id', 'winner_id', 'home_score', 'away_score']]


def get_top(n: int = 50) -> List[str]:
    data = prep_ranking()
    return [get_number_in_id(id_) for id_ in data['id'][:n]]


def make_table(n: int = 50):
    """
    Concatenates DataFrames of n ATP top players results into a single table.
    :return: Concatenated table of player results
    """
    return pd.concat([prep_player(player_id=player_id) for player_id in tqdm(get_top(n=n), desc='Processing players')], # type: ignore
                     axis=0)



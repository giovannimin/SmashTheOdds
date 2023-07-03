# -*- coding: utf-8 -*-
"""
Created on 24/05/2023 22:07
@author: GiovanniMINGHELLI
"""
from typing import List

import pandas as pd
from tqdm import tqdm
from datetime import date
from sources.get_data import Tennis
from sources.utils import get_number_in_id
from sources.week_calendar import get_next_seven_days

today = date.today()


def prep_daily_results(year=today.year, month=today.month, day=today.day):
    return Tennis().get_daily_results(year=year, month=month, day=day)


def get_weekly_schedule():
    df_list = []
    for date in get_next_seven_days():
        year, month, day = date.split('-')
        reponse = Tennis().get_daily_schedule(year=int(year), month=int(month), day=int(day))
        a = pd.DataFrame(reponse.json()['sport_events'])
        a = a[(a['status'] == 'not_started') & (a['sport_event_type'] == 'singles')]
        b = pd.concat([a, a['competitors'].apply(pd.Series)], axis=1).drop('competitors', axis=1)
        b = b.rename(columns={'id': 'match_id'})
        c = pd.concat([b, b.iloc[:, -1].apply(pd.Series)], axis=1)
        c = c.rename(columns={'id': 'player1_id'})
        d = pd.concat([c, b.iloc[:, -2].apply(pd.Series)], axis=1)
        d = d.rename(columns={'id': 'player2_id'})
        df_list.append(d.reset_index(drop=True))
    return pd.concat(df_list, axis=0)


def get_match_proba(match_id: int) -> tuple:
    match = Tennis().get_match_proba(match_id=match_id)
    home = match.json()['probabilities']['markets'][-1]['outcomes'][0]['probability']
    away = match.json()['probabilities']['markets'][-1]['outcomes'][1]['probability']
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
    # Obtenir les données de classement
    ranking_data = pd.DataFrame(Tennis().get_ranking().json()['rankings'])
    # Filtrer les données pour la compétition 'ATP'
    data = pd.DataFrame(ranking_data.loc[ranking_data['name'] == 'ATP', 'player_rankings'].iloc[0])
    # Étendre le DataFrame avec les informations du joueur
    data = pd.concat([data, data['player'].apply(pd.Series)], axis=1)
    # Supprimer les colonnes indésirables
    data.drop(['player', 'name', 'nationality', 'country_code', 'abbreviation'], axis=1, inplace=True)
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
    return pd.concat([prep_player(player_id=player_id) for player_id in tqdm(get_top(n=n), desc='Processing players')],
                     axis=0)

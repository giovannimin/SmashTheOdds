# -*- coding: utf-8 -*-
"""
Created on 25/05/2023 16:26
@author: GiovanniMINGHELLI
"""

import pytest
from sources.preprocessor import *


def test_prep_competition():
    # Appeler la fonction à tester
    result = prep_competition()
    # Vérifier que le résultat est du type DataFrame
    assert isinstance(result, pd.DataFrame)
    # Vérifier que les colonnes attendues sont présentes dans le DataFrame résultant
    expected_columns = ['tournament_id', 'type', 'gender', 'country_format', 'parent_id',
                        'season_id', 'start_date', 'end_date', 'year', 'category_id', 'name',
                        'level']
    assert result.columns.tolist() == expected_columns

    # Vérifier que seules les lignes avec 'name' égal à 'ATP' sont présentes dans le DataFrame résultant
    assert all(result['name'] == 'ATP')


def test_prep_ranking():
    # Appeler la fonction à tester
    result = prep_ranking()
    # Vérifier que le résultat est du type DataFrame
    assert isinstance(result, pd.DataFrame)
    # Vérifier que les colonnes attendues sont présentes dans le DataFrame résultant
    expected_columns = ['rank', 'points', 'ranking_movement', 'tournaments_played', 'id']
    assert result.columns.tolist() == expected_columns


def test_prep_player():
    # Appeler la fonction à tester
    result = prep_player(407573)

    # Vérifier que le résultat est du type DataFrame
    assert isinstance(result, pd.DataFrame)

    # Vérifier que les colonnes attendues sont présentes dans le DataFrame résultant
    expected_columns = ['match_id', 'scheduled', 'player1_id', 'player2_id', 'winner_id', 'home_score', 'away_score']
    assert result.columns.tolist() == expected_columns


if __name__ == '__main__':
    pytest.main()

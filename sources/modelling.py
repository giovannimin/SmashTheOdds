# -*- coding: utf-8 -*-
"""
Created on 05/07/2023 16:43
@author: GiovanniMINGHELLI
"""
import os
from sources.data_pipeline import global_transformer, next_events, history
from sources.utils import calculate_odds, get_last_model, get_root
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import joblib
from datetime import datetime
from sklearn.model_selection import GridSearchCV



def modelling():
    # Étape 1 : Préparation des données d'entraînement et de validation
    train_set, val_set = global_transformer(history()), global_transformer(next_events())

    X, y = train_set.drop('winner_is', axis=1), train_set['winner_is']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Étape 2 : Recherche des meilleurs hyperparamètres
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 5, 10],
        'min_samples_split': [2, 5, 10]}

    grid_search = GridSearchCV(estimator=RandomForestClassifier(), param_grid=param_grid, cv=5)
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    # Étape 3 : Évaluation du meilleur modèle
    print(classification_report(y_test, best_model.predict(X_test)))

    # Étape 4 : Prédiction et calcul des cotes
    results = val_set.copy()
    results['classe'], results['proba'] = best_model.predict(results), best_model.predict_proba(results)[:, 1].round(2)
    results['odds'] = calculate_odds(results['proba']).round(2)

    # Étape 5 : Suppresion de l'ancien modèle
    os.remove(get_last_model())

    # Étape 6 : Enregistrement des résultats et du modèle
    results.to_csv(os.path.join(get_root(), 'predicted_table.csv'), mode='a', header=True, index=False)
    # Ajouter la colonne des sr:match_id
    joblib.dump(value=best_model, filename=f'model_rf_{datetime.now().strftime("%Y-%m-%d")}.joblib')


if __name__ == '__main__':
    modelling()

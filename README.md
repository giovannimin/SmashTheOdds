# SmashTheOdds
It is a machine learning project that predicts tennis match scores. By analyzing player rankings, historical performance, and other key factors, it provides insights into the possible outcomes of tennis matches. The goal is to help users make more informed decisions when betting on tennis matches.
The project is based on getting tennis matches infos from SportRadar-TennisAPI and use them to predict the results of the next week matches.
The prediction is based on a RandomForest classifier with the best hyperparameters (but can be adjusted if you want to increase the performance of the model).
In order to keep the dataset up to date, data are extracted every sunday from the API and model is also trained again to reflect matches results. 

GAME SET & BET 🎾


## Getting Started

These instructions allow you to run a copy of the project locally on your system for development and testing purposes. Refer to the "Deployment" section for the steps to follow to deploy the project in production.
### Prerequisites

To run the SmashTheOdds project locally, you must :

1. Clone the repository `git clone https://github.com/giovannimin/SmashTheOdds.git`
2. Install python libraries needed  `pip install requirements.txt`
3. Create token.txt file on root and paste token from [SportRadar-TennisAPI](https://developer.sportradar.com)

### Installation

Here are the steps you need to follow to have an operational development and test environment:

```
docker-compose up --build
```
this is the only command needed to get started with FastAPI in frontend


## Running tests

```
python3 -m pytest tests/                                                                                                                                                                                      ─╯
```


## Playing and Bet



```
A définir
```

## Technologies :

* fastAPI as interface to visualize result
* Docker for containerization
* Airflow for orchestration

## Contribution

Please feel free to submit issues and feature requests!

## Credits

* **[Duhin Lucie](https://linkedin.com)**
* **[Minghelli Giovanni](https://linkedin.com)**


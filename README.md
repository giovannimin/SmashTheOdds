# SmashTheOdds
It is a machine learning project that predicts tennis match scores. By analyzing player rankings, historical performance, and other key factors, it provides insights into the possible outcomes of tennis matches. The goal is to help users make more informed decisions when betting on tennis matches.
The project is based on getting tennis matches infos from SportRadar-TennisAPI and use them to predict the results of the next week matches.
The prediction is based on a RandomForest classifier with the best hyperparameters (but can be adjusted if you want to increase the performance of the model).
In order to keep the dataset up to date, data are extracted every sunday from the API and model is also trained again to reflect matches results. 

GAME SET & BET 🎾


## Getting Started

These instructions allow you to run a copy of the project locally on your system for development and testing purposes. Refer to the "Deployment" section for the steps to follow to deploy the project in production.
### Prerequisites and installation

To run the SmashTheOdds project, you must :

1. Clone the repository `git clone https://github.com/giovannimin/SmashTheOdds.git`
2. Install python libraries needed  `pip install requirements.txt`
3. Create token.txt file on root and paste token from [SportRadar-TennisAPI](https://developer.sportradar.com)
4. install Ansible and Docker tool to run the entire project (otherwise you can also run the API locally with command in prompt


## Running tests

```
python3 -m pytest tests/                                                                                                                                                                                      ─╯
```


## Playing and Bet


As soon as everything is correctly installed you can knwo open the API and play with the tool by entering a match_id found in the planning_table.csv and then the API will return the class if player 1 is winner (class 0 is lost, class 1 if won), then you can get the probability to entere in the class and then the odds
let's play!

## Technologies :

* fastAPI as interface to visualize result
* Docker for containerization
* Apache-Airflow for orchestration
* gitActions for test

## Contribution

Please feel free to submit issues and feature requests!

## Credits

* **[Duhin Lucie](www.linkedin.com/in/lucie-duhin-0b6252a1)**
* **[Minghelli Giovanni](linkedin.com/in/giovanni-m-069320290)**


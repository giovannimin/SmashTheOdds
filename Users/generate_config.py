import csv
import os
from sources.utils import get_root


def generate_config(csv_filename, config_filename):
    users = {}
    with open(csv_filename, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users[row["username"]] = {
                "username": row["username"],
                "password": row["password"],
            }

    with open(config_filename, mode="w") as configfile:
        configfile.write(f"USERS = {users}\n")

if __name__ == "__main__":
    csv_path = os.path.join(get_root(), 'users.csv')
    generate_config(csv_path, "config.py")

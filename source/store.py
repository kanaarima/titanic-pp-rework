import titanic
import shutil
import json
import os

def store():
    shutil.rmtree("cache",ignore_errors=True)
    os.makedirs("cache/users/", exist_ok=True)
    for mode in range(4):
        leaderboard = titanic.get_leaderboard(mode)
        with open(f"cache/lb_{mode}.json", "w") as f:
            json.dump(leaderboard, f, indent=4)
        for user in leaderboard:
            plays = titanic.get_plays(user["user_id"], mode)
            with open(f"cache/users/{user['user_id']}_{mode}.json", "w") as f:
                json.dump(plays, f, indent=4)
        
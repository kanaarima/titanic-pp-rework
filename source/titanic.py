from typing import *
import requests
import time

# This is not supposed to represent the entire object since its not needed 

class Stats(TypedDict):
    
    pp: int

class User(TypedDict):
    
    id: int
    name: str
    stats: List[Stats]

class RankingEntry(TypedDict):
    
    global_rank: int
    user_id: int
    score: float # pp
    user: User

class Beatmap(TypedDict):
    
    id: int
    filename: str

class Score(TypedDict):
    
    acc: float
    max_combo: int
    mode: int
    mods: int
    n300: int
    n100: int
    n50: int
    nMiss: int
    nGeki: int
    nKatu: int
    pp: float
    beatmap: Beatmap
    id: int
    user_id: int

modes = ["osu", "taiko", "fruits", "mania"]

def get_leaderboard(mode: int = 0) -> List[RankingEntry] | None:
    req = requests.get(f"https://osu.lekuru.xyz/api/rankings/performance/{modes[mode]}")
    if not req.ok:
        return None
    return req.json()

def get_plays(user_id: int, mode: int, pages = 2) -> List[Score]:
    res = list()
    page = 1
    while True:
        req = requests.get(f"https://osu.lekuru.xyz/api/profile/{user_id}/top/{modes[mode]}?limit=50&offset={(page-1)*50}")
        if not req.ok:
            break
        data = req.json()
        res.extend(data)
        if len(data) != 50 or page == pages:
            break
        page += 1
        time.sleep(0.5)
    return res
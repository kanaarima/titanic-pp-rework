from titanic import Score, RankingEntry
from typing import *
import shutil
import store
import json
import os

def recalc():
    if not os.path.exists("cache/"):
        print("Fetching plays...")
        store.store()
    
    shutil.rmtree("output", ignore_errors=True)
    os.makedirs("output/users/", exist_ok=True)

    def handle_recalc(score: Score) -> float:
        match score['mode']:
            case 0:
                return recalc_osu(score)
            case 1:
                return recalc_taiko(score)
            case 2:
                return recalc_ctb(score)
            case 3:
                return recalc_mania(score)

    for mode in range(4):
        
        print(f"Recalcing mode {mode}")
        
        with open(f"cache/lb_{mode}.json") as f:
            leaderboard: List[RankingEntry] = json.load(f)
        
        new_leaderboard = list()
        
        for user in leaderboard:
            
            with open(f"cache/users/{user['user_id']}_{mode}.json") as f:
                scores: List[Score] = json.load(f)
            
            if not scores:
                continue
            
            new_scores = list()
            
            for score in scores:
                new_pp = handle_recalc(score)
                new_score = score.copy()
                new_score['pp'] = new_pp
                new_scores.append(new_score)
            new_scores.sort(key=lambda x: x['pp'], reverse=True)
            
            with open(f"output/users/{user['user_id']}_{mode}.json", "w") as f:
                json.dump(new_scores, f, indent=4)
            
            new_total_pp = 0
            old_total_pp = 0
            
            for x in range(min(100, len(new_scores))):
                new_total_pp += new_scores[x]['pp'] * 0.95 ** x
                        
            for x in range(min(100, len(scores))):
                old_total_pp += scores[x]['pp'] * 0.95 ** x

            entry = user.copy()
            entry['score'] = new_total_pp
            new_leaderboard.append(entry)
        
            print(f"{user['user']['name']}: {old_total_pp:.0f}pp -> {new_total_pp:.0f}pp (Top play: {scores[0]['pp']:.0f} -> {new_scores[0]['pp']:.0f})")

        new_leaderboard.sort(key=lambda x: x['score'], reverse=True)
        rank = 1

        # recalc global rank
        for entry in new_leaderboard:
            entry['global_rank'] = rank
            rank += 1

        with open(f"output/lb_{mode}.json", "w") as f:
            json.dump(new_leaderboard, f, indent=4)

def recalc_osu(score: Score):
    return score['pp']

def recalc_taiko(score: Score):
    return score['pp']

def recalc_ctb(score: Score):
    return score['pp']

def recalc_mania(score: Score):
    return score['pp']
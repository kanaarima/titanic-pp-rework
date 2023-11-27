from titanic_pp_py import Calculator as titanic_calculator
from titanic_pp_py import Beatmap as titanic_beatmap

from rosu_pp_py import Calculator as rosu_calculator
from rosu_pp_py import Beatmap as rosu_beatmap

from titanic import Score, RankingEntry
from typing import *

import requests
import shutil
import store
import json
import time
import os

def recalc():
    if not os.path.exists("cache/"):
        print("Fetching plays...")
        store.store()
    
    shutil.rmtree("output", ignore_errors=True)
    os.makedirs("output/users/", exist_ok=True)
    os.makedirs("beatmaps/", exist_ok=True)
    
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
    if not (beatmap := get_map(score['beatmap']['id'])):
        print(f"Can't recalc score {score['id']}!")
        return score['pp']
    if score['mods'] & 128: # RX
        rounded = get_rounded_values(beatmap)
        map = titanic_beatmap(path = beatmap)
        for k, v in rounded.items():
            match k:
                case "ar":
                    map.set_ar(v)
                case "od":
                    map.set_od(v)
                case "hp":
                    map.set_hp(v)
                case "cs":
                    map.set_cs(v)
        calc = titanic_calculator(mods=score['mods'], mode=score['mode'])
        calc.set_combo(score['max_combo'])
        calc.set_n300(score['n300'])
        calc.set_n100(score['n100'])
        calc.set_n50(score['n50'])
        calc.set_n_misses(score['nMiss'])
        calc.set_n_geki(score['nGeki'])
        calc.set_n_katu(score['nKatu'])
        return calc.performance(map).pp
    else:
        rounded = get_rounded_values(beatmap)
        map = rosu_beatmap(path = beatmap)
        for k, v in rounded.items():
            match k:
                case "ar":
                    map.set_ar(v)
                case "od":
                    map.set_od(v)
                case "hp":
                    map.set_hp(v)
                case "cs":
                    map.set_cs(v)
        calc = rosu_calculator(mods=score['mods'], mode=score['mode'])
        calc.set_combo(score['max_combo'])
        calc.set_n300(score['n300'])
        calc.set_n100(score['n100'])
        calc.set_n50(score['n50'])
        calc.set_n_misses(score['nMiss'])
        calc.set_n_geki(score['nGeki'])
        calc.set_n_katu(score['nKatu'])
        return calc.performance(map).pp

def recalc_taiko(score: Score):
    if not (beatmap := get_map(score['beatmap']['id'])):
        print(f"Can't recalc score {score['id']}!")
        return score['pp']
    if score['mods'] & 128: # RX
        rounded = get_rounded_values(beatmap)
        map = titanic_beatmap(path = beatmap)
        for k, v in rounded.items():
            match k:
                case "ar":
                    map.set_ar(v)
                case "od":
                    map.set_od(v)
                case "hp":
                    map.set_hp(v)
                case "cs":
                    map.set_cs(v)
        calc = titanic_calculator(mods=score['mods'], mode=score['mode'])
        calc.set_combo(score['max_combo'])
        calc.set_n300(score['n300'])
        calc.set_n100(score['n100'])
        calc.set_n50(score['n50'])
        calc.set_n_misses(score['nMiss'])
        calc.set_n_geki(score['nGeki'])
        calc.set_n_katu(score['nKatu'])
        return calc.performance(map).pp
    else:
        rounded = get_rounded_values(beatmap)
        map = rosu_beatmap(path = beatmap)
        for k, v in rounded.items():
            match k:
                case "ar":
                    map.set_ar(v)
                case "od":
                    map.set_od(v)
                case "hp":
                    map.set_hp(v)
                case "cs":
                    map.set_cs(v)
        calc = rosu_calculator(mods=score['mods'], mode=score['mode'])
        calc.set_combo(score['max_combo'])
        calc.set_n300(score['n300'])
        calc.set_n100(score['n100'])
        calc.set_n50(score['n50'])
        calc.set_n_misses(score['nMiss'])
        calc.set_n_geki(score['nGeki'])
        calc.set_n_katu(score['nKatu'])
        return calc.performance(map).pp

def recalc_ctb(score: Score):
    if not (beatmap := get_map(score['beatmap']['id'])):
        print(f"Can't recalc score {score['id']}!")
        return score['pp']
    if score['mods'] & 128: # RX
        rounded = get_rounded_values(beatmap)
        map = titanic_beatmap(path = beatmap)
        for k, v in rounded.items():
            match k:
                case "ar":
                    map.set_ar(v)
                case "od":
                    map.set_od(v)
                case "hp":
                    map.set_hp(v)
                case "cs":
                    map.set_cs(v)
        calc = titanic_calculator(mods=score['mods'], mode=score['mode'])
        calc.set_combo(score['max_combo'])
        calc.set_n300(score['n300'])
        calc.set_n100(score['n100'])
        calc.set_n50(score['n50'])
        calc.set_n_misses(score['nMiss'])
        calc.set_n_geki(score['nGeki'])
        calc.set_n_katu(score['nKatu'])
        return calc.performance(map).pp
    else:
        rounded = get_rounded_values(beatmap)
        map = rosu_beatmap(path = beatmap)
        for k, v in rounded.items():
            match k:
                case "ar":
                    map.set_ar(v)
                case "od":
                    map.set_od(v)
                case "hp":
                    map.set_hp(v)
                case "cs":
                    map.set_cs(v)
        calc = rosu_calculator(mods=score['mods'], mode=score['mode'])
        calc.set_combo(score['max_combo'])
        calc.set_n300(score['n300'])
        calc.set_n100(score['n100'])
        calc.set_n50(score['n50'])
        calc.set_n_misses(score['nMiss'])
        calc.set_n_geki(score['nGeki'])
        calc.set_n_katu(score['nKatu'])
        return calc.performance(map).pp

def recalc_mania(score: Score):
    if not (beatmap := get_map(score['beatmap']['id'])):
        print(f"Can't recalc score {score['id']}!")
        return score['pp']
    rounded = get_rounded_values(beatmap)
    map = rosu_beatmap(path = beatmap)
    for k, v in rounded.items():
        match k:
            case "ar":
                map.set_ar(v)
            case "od":
                map.set_od(v)
            case "hp":
                map.set_hp(v)
            case "cs":
                map.set_cs(v)
    calc = rosu_calculator(mods=score['mods'], mode=score['mode'])
    calc.set_combo(score['max_combo'])
    calc.set_n300(score['n300'])
    calc.set_n100(score['n100'])
    calc.set_n50(score['n50'])
    calc.set_n_misses(score['nMiss'])
    calc.set_n_geki(score['nGeki'])
    calc.set_n_katu(score['nKatu'])
    return calc.performance(map).pp
def get_rounded_values(beatmap_path):
    res = {}
    with open(beatmap_path) as f:
        for line in f.readlines():
            line = line.strip().split(":")
            if len(line) != 2:
                continue
            match line[0]:
                case "OverallDifficulty":
                    res['od'] = round(float(line[1]))
                case "CircleSize":
                    res['cs'] = round(float(line[1]))
                case "HPDrainRate":
                    res['hp'] = round(float(line[1]))
                case "ApproachRate":
                    res['ar'] = round(float(line[1]))
    return res

def get_map(beatmap_id) -> str | None:
    if os.path.exists(f"beatmaps/{beatmap_id}.osu"):
        return f"beatmaps/{beatmap_id}.osu"
    req = requests.get(f"https://old.ppy.sh/osu/{beatmap_id}")
    time.sleep(0.5)
    if not req.ok:
        return
    with open(f"beatmaps/{beatmap_id}.osu", "wb") as f:
        f.write(req.content)
    return f"beatmaps/{beatmap_id}.osu"

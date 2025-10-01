import json
import random

########## Database ##########

def return_tournaments_list():
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        tournaments_list = [tournament["name"] for tournament in tournaments]
        file.close()
    return tournaments_list

def create_tournament(name, rounds, tables):
    if check_tournament_entry(name, rounds, tables) is True:
        with open("db.json", "r") as file:
            data = json.load(file)

        if "tournaments" not in data:
            data["tournaments"] = []

        total_rounds = int(rounds.get().strip())
        total_tables = int(tables.get().strip())

        new_rounds = []
        for i in range(1, total_rounds + 1):
            new_rounds.append({
                "nb": i,
                "teams_points": []
            })

        new_tables = []
        for i in range(1, total_rounds + 1):
            round_tables = {
                "round": i,
                "repartition": []
            }
            for j in range(1, total_tables + 1):
                round_tables["repartition"].append({
                    "tablenumber": j,
                    "teams": []
                })
            new_tables.append(round_tables)

        new_tournament = {
            "name": name.get().strip(),
            "rounds_number": total_rounds,
            "rounds": new_rounds,
            "tables": new_tables,
            "status": False,
            "teams": []
        }

        data["tournaments"].insert(0, new_tournament)

        with open("db.json", "w") as file:
            json.dump(data, file, indent=4)


def check_tournament(tournament):
    try:
        tournament = tournament[0]
    except IndexError:
        print("Aucun tournois sélectionné.")
        return False
    
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        file.close()

    for t in tournaments:
        if t["name"] == tournament:
            return True
        
def get_tournament(tournament):
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        file.close()

    for t in tournaments:
        if t["name"] == tournament:
            t = {
                "name": t["name"],
                "rounds_number": t["rounds_number"],
                "rounds": t["rounds"],
                "tables": t["tables"],
                "status": t["status"],
                "teams": [
                    f"{team[2]} - {team[0]} - {team[1]}" for team in t["teams"]
                ]
            }
            
            return t
        
def return_rounds_points(tournament):
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        file.close()

    for t in tournaments:
        if t["name"] == tournament:
            rounds_points = []
            for round_info in t["rounds"]:
                points = {team["team_id"]: team["points"] for team in round_info["teams_points"]}
                rounds_points.append({
                    "round": round_info["nb"],
                    "points": points
                })
            return rounds_points
    return []

def return_tournament_teams(tournament):
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        file.close()

    for t in tournaments:
        if t["name"] == tournament:
            return t["teams"]
        
def get_next_team_number(tournament):
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        file.close()

    for t in tournaments:
        if t["name"] == tournament:
            if not t["teams"]:
                return 1
            else:
                last_team = t["teams"][-1]
                return last_team[2] + 1
    return 1

def create_team(player1, player2, teamid, tournament):
    with open("db.json", "r") as file:
        data = json.load(file)
        tournaments = data.get("tournaments", [])
        file.close()

    for t in tournaments:
        if t["name"] == tournament:
            t["teams"].append([player1.get().strip(), player2.get().strip(), int(teamid)])
            break

    with open("db.json", "w") as file:
        json.dump(data, file, indent=4)


########## Misc ##########

def check_tournament_entry(name, rounds, tables):
    tournament_name = name.get().strip()
    rounds_number = rounds.get().strip()
    table_number = tables.get().strip()

    if tournament_name == "" or rounds_number == "" or table_number == "":
        print("Il manque des informations pour la création du tournois.")
        return False
    
    try:
        rounds_number = int(rounds_number)
    except ValueError:
        print("Le nombre de tours doit être un entier.")
        return False

    try:
        table_number = int(table_number)
    except ValueError:
        print("Le nombre de tables doit être un entier.")
        return False
    
    return True

def generate_team_repartition(round_number, teams, tournament_name):
    table_needed = len(teams) // 2

    with open("db.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    tournament = next((t for t in data["tournaments"] if t["name"] == tournament_name), None)
    if tournament is None:
        print(f"Tournament '{tournament_name}' not found.")
        return []

    if round_number == 1:
        pairs = random.sample(teams, len(teams))
        repartition = []
        for i in range(table_needed):
            repartition.append({
                "tablenumber": i + 1,
                "teams": [pairs[i * 2], pairs[i * 2 + 1]]
            })
            
    else:
        past_pairings = set()
        for table_round in tournament.get("tables", []):
            if table_round["round"] < round_number:
                for table in table_round["repartition"]:
                    if len(table["teams"]) == 2:
                        ids = sorted([table["teams"][0][2], table["teams"][1][2]])
                        past_pairings.add(tuple(ids))

        max_attempts = 1000000
        for _ in range(max_attempts):
            pairs = random.sample(teams, len(teams))
            valid = True
            temp_repartition = []

            for i in range(table_needed):
                team1 = pairs[i * 2]
                team2 = pairs[i * 2 + 1]
                team_ids = tuple(sorted([team1[2], team2[2]]))
                if team_ids in past_pairings:
                    valid = False
                    break
                temp_repartition.append({
                    "tablenumber": i + 1,
                    "teams": [team1, team2]
                })

            if valid:
                repartition = temp_repartition
                break
        else:
            raise Exception("Unable to generate a valid repartition without repeating past pairings.")

    for table_round in tournament.get("tables", []):
        if table_round["round"] == round_number:
            for table in table_round["repartition"]:
                tablenum = table["tablenumber"]
                if 1 <= tablenum <= table_needed:
                    table["teams"] = repartition[tablenum - 1]["teams"]
                else:
                    table["teams"] = []

    with open("db.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return repartition

def generate_leaderboard(tournament_name):
    with open("db.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    tournament = next((t for t in data["tournaments"] if t["name"] == tournament_name), None)
    if not tournament:
        return []

    team_points_map = {}

    for team in tournament["teams"]:
        team_id = team[2]
        team_name = f"{team_id} - {team[0]} - {team[1]}"
        team_points_map[team_id] = {
            "team": team_name,
            "points": 0
        }

    for round_info in tournament.get("rounds", []):
        for team_score in round_info.get("teams_points", []):
            team_id = team_score["team_id"]
            points = team_score["points"]
            if team_id in team_points_map:
                team_points_map[team_id]["points"] += points

    leaderboard = sorted(team_points_map.values(), key=lambda x: x["points"], reverse=True)
    return leaderboard

def start_next_round(entries, round_number, tournament_name):
    teampoints = []

    table_needed = int(len(entries))

    for i in range(table_needed):
        table_number = i + 1

        try:
            teampoint1 = int(entries[table_number]["team1"].get())
            teampoint2 = int(entries[table_number]["team2"].get())
        except ValueError:
            print(f"Invalid input at table {table_number}. Skipping.")
            continue

        teampoints.append((table_number, teampoint1, teampoint2))

    with open("db.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tournament = next((t for t in data["tournaments"] if t["name"] == tournament_name), None)
    if not tournament:
        print(f"Tournament '{tournament_name}' not found.")
        return False

    tables_round = next((tr for tr in tournament["tables"] if tr["round"] == round_number), None)
    if not tables_round:
        print(f"Table info for round {round_number} not found.")
        return False

    round_entry = next((r for r in tournament["rounds"] if r["nb"] == round_number), None)
    if not round_entry:
        round_entry = {"nb": round_number, "teams_points": []}
        tournament["rounds"].append(round_entry)

    for tablenumber, pt1, pt2 in teampoints:
        try:
            table = next(t for t in tables_round["repartition"] if t["tablenumber"] == tablenumber)
            team1_id = table["teams"][0][2]
            team2_id = table["teams"][1][2]

            round_entry["teams_points"].append({"team_id": team1_id, "points": pt1})
            round_entry["teams_points"].append({"team_id": team2_id, "points": pt2})
        except (IndexError, StopIteration):
            print(f"Could not retrieve team IDs for table {tablenumber}.")
            continue

    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return tournament["rounds_number"]
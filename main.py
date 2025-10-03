################################################################################################################################################
#                                                                                                                                              #
#                                                                                                                                              #
#                                                       Projet for Belotte Tournament                                                          #
#                                                              Use as you want                                                                 #
#                                                                                                                                              #
#                                                                                                                                              #
################################################################################################################################################


import customtkinter
from CTkTable import *

from functions import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


########## Scrollable Frames ##########

class FrameTournoisPrecedents(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    
class FrameEquipes(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


########## Windows ##########

class MenuTournois(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tournois Belotte - Liste des tournois")
        self.geometry("500x400")
        self.grid_columnconfigure((0, 1), weight=1)

        self.title = customtkinter.CTkLabel(self, text="Tournois Belotte - Liste des tournois", font=("Arial", 20))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        create_db()
        
        self.tournaments_list = return_tournaments_list() 

        self.build_ui()

    def build_ui(self):
        ##### Tournaments List #####

        self.scrollable_checkbox_frame = FrameTournoisPrecedents(self, title="Tournois", values=self.tournaments_list)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.loadtournamentbutton = customtkinter.CTkButton(self, text="Ouvrir tournois", command=self.open_tournament)
        self.loadtournamentbutton.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=1)


        ##### Create Tournament #####

        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="n")

        self.right_inner_frame = customtkinter.CTkFrame(self.right_frame, fg_color="transparent")
        self.right_inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.title_bar = customtkinter.CTkFrame(self.right_inner_frame, fg_color="#3a3a3a", corner_radius=6)
        self.title_bar.pack(fill="x", pady=(0, 20))

        self.createtournamentlabel = customtkinter.CTkLabel(self.title_bar, text="Créer un nouveau tournois", font=("Arial", 14))
        self.createtournamentlabel.pack(padx=10, pady=5)

        self.tournamentname = customtkinter.CTkEntry(self.right_inner_frame, placeholder_text="Nom du tournois")
        self.tournamentname.pack(pady=(0, 20), fill="x")

        self.roundsnumber = customtkinter.CTkEntry(self.right_inner_frame, placeholder_text="Nombre de tours")
        self.roundsnumber.pack(pady=(0, 20), fill="x")

        self.tablenumber = customtkinter.CTkEntry(self.right_inner_frame, placeholder_text="Nombre de tables")
        self.tablenumber.pack(pady=(0, 20), fill="x")

        self.createtournamentbutton = customtkinter.CTkButton(self, text="Créer le tournois", command=self.create_tournament)
        self.createtournamentbutton.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

    def create_tournament(self):
        create_tournament(self.tournamentname, self.roundsnumber, self.tablenumber)

        self.scrollable_checkbox_frame.destroy()
        self.scrollable_checkbox_frame = FrameTournoisPrecedents(self, title="Tournois", values=return_tournaments_list())
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def open_tournament(self):
        tournament_check = FrameTournoisPrecedents.get(self.scrollable_checkbox_frame)

        if check_tournament(tournament_check) == True:
            tournament_data = get_tournament(tournament_check[0])

            Equipes(tournament_data).mainloop()


class Equipes(customtkinter.CTk):
    def __init__(self, tournament_data):
        super().__init__()

        self.title("Tournois Belotte - Liste des équipes")
        self.geometry("500x400")
        self.grid_columnconfigure((0, 1), weight=1)

        self.tournament_data = tournament_data
        self.teams_list = self.tournament_data["teams"]

        self.build_ui()


    def build_ui(self):
        self.title = customtkinter.CTkLabel(self, text="Tournois Belotte - Liste des équipes", font=("Arial", 20))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)


        ##### Teams list #####

        self.scrollable_checkbox_frame = FrameEquipes(self, title="Équipes", values=self.teams_list)
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.starttournois = customtkinter.CTkButton(self, text="Commencer le tournois", command=self.start_tournament)
        self.starttournois.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=1)


        ##### Create team #####

        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="n")

        self.right_inner_frame = customtkinter.CTkFrame(self.right_frame, fg_color="transparent")
        self.right_inner_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.title_bar = customtkinter.CTkFrame(self.right_inner_frame, fg_color="#3a3a3a", corner_radius=6)
        self.title_bar.pack(fill="x", pady=(0, 20))

        self.createteamlabel = customtkinter.CTkLabel(self.title_bar, text="Créer une équipe", font=("Arial", 14))
        self.createteamlabel.pack(padx=10, pady=5)

        self.teamplayer1 = customtkinter.CTkEntry(self.right_inner_frame, placeholder_text="Joueur 1")
        self.teamplayer1.pack(pady=(0, 20), fill="x")

        self.teamplayer2 = customtkinter.CTkEntry(self.right_inner_frame, placeholder_text="Joueur 2")
        self.teamplayer2.pack(pady=(0, 20), fill="x")

        self.createteambutton = customtkinter.CTkButton(self, text="Créer l'équipe", command=self.create_team)
        self.createteambutton.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

    def create_team(self):
        self.teamid = get_next_team_number(self.tournament_data["name"])
        create_team(self.teamplayer1, self.teamplayer2, int(self.teamid), self.tournament_data["name"])

        self.scrollable_checkbox_frame.destroy()
        self.scrollable_checkbox_frame = FrameEquipes(self, title="Équipes", values=return_tournament_teams(self.tournament_data["name"]))
        self.scrollable_checkbox_frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

    def start_tournament(self):
        Rounds(1, self.tournament_data["name"]).mainloop()

class Rounds(customtkinter.CTk):
    def __init__(self, round_number, tournament_name):
        super().__init__()
        self.title("Tournois Belotte - Parties")
        self.geometry("1920x1080")
        # self.attributes("-fullscreen", "True")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.tournament_name = tournament_name
        self.round_number = round_number
        self.entries = {}
        self.table_needed = int(len(return_tournament_teams(self.tournament_name))) / 2
        self.repartition = generate_team_repartition(self.round_number, return_tournament_teams(self.tournament_name), self.tournament_name)

        self.build_ui()


    def build_ui(self):
        self.title = customtkinter.CTkLabel(self, text=f"Tournois Belotte - Round {self.round_number}", font=("Arial", 20))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        for i in range(int(self.table_needed)):
            table_number = i + 1
            team1 = self.repartition[i]["teams"][0]
            team2 = self.repartition[i]["teams"][1]

            team1_infos = f"{team1[2]} - {team1[0]} - {team1[1]}"
            team2_infos = f"{team2[2]} - {team2[0]} - {team2[1]}"

            round_frame = customtkinter.CTkFrame(self.scrollable_frame, height=100, fg_color="#2b2b2b")
            round_frame.grid(row=i, column=0, padx=10, pady=20, sticky="ew")
            round_frame.grid_propagate(False)
            round_frame.grid_columnconfigure(2, weight=1) 

            team1_label = customtkinter.CTkLabel(round_frame, text=f"{team1_infos}", font=("Arial", 16))
            team1_label.grid(row=0, column=0, padx=20, pady=35, sticky="w")

            team1_points_entry = customtkinter.CTkEntry(round_frame, placeholder_text="Points", width=100)
            team1_points_entry.grid(row=0, column=1, padx=20, pady=35, sticky="e")

            table_label = customtkinter.CTkLabel(round_frame, text=f"Table {table_number}", font=("Arial", 16), anchor="center")
            table_label.grid(row=0, column=2, padx=20, pady=35, sticky="ew")

            team2_label = customtkinter.CTkLabel(round_frame, text=f"{team2_infos}", font=("Arial", 16))
            team2_label.grid(row=0, column=4, padx=20, pady=35, sticky="e")

            team2_points_entry = customtkinter.CTkEntry(round_frame, placeholder_text="Points", width=100)
            team2_points_entry.grid(row=0, column=3, padx=20, pady=35, sticky="e")

            self.entries[table_number] = {
                "team1": team1_points_entry,
                "team2": team2_points_entry
            }

        self.next_round_button = customtkinter.CTkButton(self, text="Prochaine manche", command=self.next_round)
        self.next_round_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.table_button = customtkinter.CTkButton(self, text="Créer tableau", command=self.roundstable)
        self.table_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

    def next_round(self):
        total_rounds = start_next_round(self.entries, self.round_number, self.tournament_name)

        if not total_rounds:
            return

        if total_rounds == self.round_number:
            Leaderboard(self.tournament_name).mainloop()
            self.destroy()
        else:
            self.destroy()
            Rounds(self.round_number + 1, self.tournament_name).mainloop()

    def roundstable(self):
        if self.round_number == 1:
            RoundsTable(len(return_tournament_teams(self.tournament_name)), self.repartition, None, self.tournament_name).mainloop()
        else:
            RoundsTable(len(return_tournament_teams(self.tournament_name)), self.repartition, return_rounds_points(self.tournament_name), self.tournament_name).mainloop()

class RoundsTable(customtkinter.CTk):
    def __init__(self, team_number, repartition, points, tournament_name):
        super().__init__()
        self.title("Tournois Belotte - Rounds")
        self.geometry("1920x1080")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1) 

        self.team_number = team_number
        self.table_needed = self.team_number // 2
        self.repartition = repartition
        self.position = 0
        self.points = points
        self.tournament_name = tournament_name
        self.classement = generate_leaderboard(self.tournament_name)
        self.left_header = [["Numéro d'Equipe", "Partie 1", "Partie 2", "Partie 3", "Partie 4", "Points totaux", "Classement"]]
        self.right_header = [["Equipe", "Table", "Equipe"]]

        self.build_ui()

    def build_ui(self):
        self.left_frame = customtkinter.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.left_inner_frame = customtkinter.CTkFrame(self.left_frame, fg_color="transparent")
        self.left_inner_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.left_inner_frame.grid_rowconfigure(0, weight=1)
        self.left_inner_frame.grid_columnconfigure(0, weight=1)

        self.left_table = CTkTable(master=self.left_inner_frame, row=int(self.team_number) + 1, column=0, values=self.left_header, header_color="#1f538d")
        self.left_table.grid(row=0, column=0, sticky="nsew")

        for i in range(int(self.team_number)):
            self.left_table.insert(i + 1, 0, f"{i + 1}")

        if self.points is not None:
            for entry in self.points:
                round_num = entry['round']
                points = entry['points']

                for team, score in points.items():
                    self.left_table.insert(team, round_num, score)

        for entry in self.classement:
            self.position = self.position + 1
            team_str = entry['team']
            team_number = int(team_str.split(' - ')[0])

            self.left_table.insert(team_number, 6, self.position)

            if self.points is not None:
                self.left_table.insert(team_number, 5, entry['points'])


        ################## Right frame ##################

        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.right_inner_frame = customtkinter.CTkFrame(self.right_frame, fg_color="transparent")
        self.right_inner_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.right_table = CTkTable(master=self.right_inner_frame, row=int(self.table_needed) + 1, column=0, values=self.right_header, header_color="#1f538d")
        self.right_table.grid(row=0, column=0, sticky="nsew")
        self.right_inner_frame.grid_rowconfigure(0, weight=1)
        self.right_inner_frame.grid_columnconfigure(0, weight=1)

        for i in range(int(self.table_needed)):
            team1 = self.repartition[i]["teams"][0]
            team2 = self.repartition[i]["teams"][1]

            team1_label = f"Equipe {team1[2]}"
            team2_label = f"Equipe {team2[2]}"

            self.right_table.insert(i + 1, 0, team1_label)
            self.right_table.insert(i + 1, 1, f"Table {i + 1}")
            self.right_table.insert(i + 1, 2, team2_label)


class Leaderboard(customtkinter.CTk):
    def __init__(self, tournament_name):
        super().__init__()
        self.title("Tournois Belotte - Classement")
        self.geometry("1920x1080")
        # self.attributes("-fullscreen", "True")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.tournament_name = tournament_name
        self.leaderboard_data = generate_leaderboard(tournament_name)

        self.build_ui()


    def build_ui(self):
        self.title = customtkinter.CTkLabel(self, text=f"Classement du Concours", font=("Arial", 32))
        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        for i in range(len(self.leaderboard_data)):
            position = i + 1
            round_frame = customtkinter.CTkFrame(self.scrollable_frame, height=50, fg_color="#2b2b2b")
            round_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            round_frame.grid_propagate(False)
            round_frame.grid_columnconfigure(2, weight=1) 

            position_label = customtkinter.CTkLabel(round_frame, text=f"Place {position}", font=("Arial", 18))
            position_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

            team_label = customtkinter.CTkLabel(round_frame, text=f"Equipe n°{self.leaderboard_data[i]['team']} avec {self.leaderboard_data[i]['points']} points", font=("Arial", 18), anchor="center")
            team_label.grid(row=0, column=2, padx=0, pady=10, sticky="ew")

         

if __name__ == "__main__":
    app = MenuTournois()
    app.mainloop() 
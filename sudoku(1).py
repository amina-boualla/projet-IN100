
class SudokuUI(tk.Frame):
    def __init__(self, parent, grille, solution):
        super().__init__(parent)
        self.grille = grille
        self.solution = solution 
        self.entries = [[None]*9 for _ in range(9)]

        self.create_grid()
        self.remplir()

    def create_grid(self):
        for bloc_ligne in range(3):
            for bloc_col in range(3):

                # couleur alternée pour les blocs
                bg = "#e6e6e6" if (bloc_ligne + bloc_col) % 2 == 0 else "#ffffff"

                frame = tk.Frame(self, bg=bg, bd=2, relief="solid")
                frame.grid(row=bloc_ligne, column=bloc_col, padx=2, pady=2)

                for i in range(3):
                    for j in range(3):
                        ligne = bloc_ligne * 3 + i
                        colonne = bloc_col * 3 + j

                        entry = tk.Entry(
                            frame,
                            width=2,
                            font=("Helvetica", 18, "bold"),
                            justify="center",
                            relief="flat",
                            bg=bg
                        )
                        entry.grid(row=i, column=j, padx=1, pady=1)

                        self.entries[ligne][colonne] = entry
                        entry.bind("<KeyRelease>", lambda event, l=ligne, c=colonne: self.verifier_case(l, c))
    def verifier_case(self, ligne , colonne):
        val = self.entries[ligne][colonne].get()
        if val.isdigit():
            val = int(val)
            if val == self.solution[ligne][colonne]:
                self.entries[ligne][colonne].config(fg = "black")
            else : 
                self.entries[ligne][colonne].config(fg="red")

    def remplir(self):
        for i in range(9):
            for j in range(9):
                val = self.grille[i][j]
                e = self.entries[i][j]

                e.delete(0, tk.END)

                if val != 0:
                    e.insert(0, str(val))
                    e.config(state="disabled", disabledforeground="black")
                else:
                    e.config(state="normal")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")

        self.frame_actuelle = None
        self.afficher_menu()

    def changer_frame(self, frame):
        if self.frame_actuelle:
            self.frame_actuelle.destroy()
        self.frame_actuelle = frame
        self.frame_actuelle.pack()

    def afficher_menu(self):
        frame = tk.Frame(self, bg = "lightyellow")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Choisis la difficulté", font=("Arial", 50) ,fg= "lightblue", bg = "lightyellow" ).grid(row = 0 , column=0, sticky="w", padx=20, pady=20)

        tk.Button(frame, text="Facile", bg = "white" , fg="lightblue",font =("Arial", 30),
                  command=lambda: self.lancer_jeu("Facile")).grid(row=1, column=0, pady=10, sticky="n")

        tk.Button(frame, text="Moyen",bg = "white" , fg="lightblue", font =("Arial", 30),
                  command=lambda: self.lancer_jeu("Moyen")).grid(row=2, column=0, pady=10, sticky="n")

        tk.Button(frame, text="Difficile",bg = "white" , fg="lightblue",font =("Arial", 30),
                  command=lambda: self.lancer_jeu("Difficile")).grid(row=3, column=0, pady=10, sticky="n")

        self.changer_frame(frame)

    def get_nb_cases(self, difficulte):
        if difficulte == "Facile":
            return 30
        elif difficulte == "Moyen":
            return 40
        else:
            return 50

    def lancer_jeu(self, difficulte):
        frame = tk.Frame(self, bg = "lightyellow",)
        frame.pack(fill="both", expand=True)

        # Génération Sudoku
        grille = générer_grille()
        sudoku(grille)
        solution = [ligne[:] for ligne in grille]

        nb = self.get_nb_cases(difficulte)
        efface(grille, nb)

        ui = SudokuUI(frame, grille, solution)
        ui.pack()

        tk.Button(frame, text="Retour au menu",
                  command=self.afficher_menu).pack(pady=10)

        self.changer_frame(frame)


app = App()
app.mainloop()
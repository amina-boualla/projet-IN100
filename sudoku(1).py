import tkinter as tk


class SudokuUI(tk.Frame):
    def __init__(self, parent, grille):
        super().__init__(parent)
        self.grille = grille
        self.entries = [[None]*9 for _ in range(9)]
        self.base_colors = [[None]*9 for _ in range(9)]
        self.secondes = 0
        self.chrono_label = None
        self.chrono_actif = True
        self.derniere_valeur = [[None]*9 for _ in range(9)]
        self.historique = []

        self.create_bandeau()
        self.create_grid()
        self.remplir()

    def create_bandeau(self):
        bandeau = tk.Frame(self, bg="lightyellow")
        bandeau.grid(row=0, column=0, columnspan=3, pady=(0, 8))

        self.chrono_label = tk.Label(
            bandeau, text="Temps : 00:00",
            font=("Arial", 14), bg="lightyellow"
        )
        self.chrono_label.pack(side="left", padx=20)

        self.update_chrono()

    def update_chrono(self):
        if self.chrono_actif:
            self.secondes += 1
            minutes = self.secondes // 60
            secondes = self.secondes % 60
            self.chrono_label.config(text=f"Temps : {minutes:02d}:{secondes:02d}")
            self.after(1000, self.update_chrono)

    def create_grid(self):
        for bloc_ligne in range(3):
            for bloc_col in range(3):
                bg = "#e6e6e6" if (bloc_ligne + bloc_col) % 2 == 0 else "#ffffff"

                frame = tk.Frame(self, bg=bg)
                frame.grid(row=bloc_ligne + 1, column=bloc_col)

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
                        self.base_colors[ligne][colonne] = bg

                        entry.bind(
                            "<KeyRelease>",
                            lambda event, l=ligne, c=colonne: self.verifier_case(event, l, c)
                        )
                        entry.bind(
                            "<Button-1>",
                            lambda event, l=ligne, c=colonne: self.highlight_selected(l, c)
                        )

    def set_bg(self, i, j, color):
        e = self.entries[i][j]
        if e.cget("state") == "disabled":
            e.config(disabledbackground=color)
        else:
            e.config(bg=color)

    def reset_colors(self):
        for i in range(9):
            for j in range(9):
                self.set_bg(i, j, self.base_colors[i][j])

    def highlight_selected(self, ligne, colonne):
        self.reset_colors()
        self.set_bg(ligne, colonne, "#cce6ff")

    def highlight_erreurs(self, ligne, colonne, val):
        self.reset_colors()

        for j in range(9):
            if j != colonne and self.entries[ligne][j].get() == str(val):
                self.set_bg(ligne, j, "red")

        for i in range(9):
            if i != ligne and self.entries[i][colonne].get() == str(val):
                self.set_bg(i, colonne, "red")

        start_l = 3 * (ligne // 3)
        start_c = 3 * (colonne // 3)

        for i in range(start_l, start_l + 3):
            for j in range(start_c, start_c + 3):
                if (i != ligne or j != colonne) and self.entries[i][j].get() == str(val):
                    self.set_bg(i, j, "red")

        self.set_bg(ligne, colonne, "#cce6ff")

    def verifier_case(self, event, ligne, colonne):
        if event.keysym in ("Delete", "BackSpace"):
            ancienne = self.grille[ligne][colonne]
            if ancienne != 0:
                self.historique.append((ligne, colonne, ancienne))

            self.entries[ligne][colonne].delete(0, tk.END)
            self.grille[ligne][colonne] = 0
            self.derniere_valeur[ligne][colonne] = None
            self.highlight_selected(ligne, colonne)
            return

        val = self.entries[ligne][colonne].get()

        if not val.isdigit():
            return

        if val == self.derniere_valeur[ligne][colonne]:
            return

        self.derniere_valeur[ligne][colonne] = val
        val = int(val)

        self.historique.append((ligne, colonne, self.grille[ligne][colonne]))

        self.grille[ligne][colonne] = 0

        if valide_ou_pas(self.grille, ligne, colonne, val):
            self.entries[ligne][colonne].config(fg="black")
            self.highlight_selected(ligne, colonne)
        else:
            self.entries[ligne][colonne].config(fg="red")
            self.highlight_erreurs(ligne, colonne, val)

        self.grille[ligne][colonne] = val

    def annuler(self):
        if not self.historique:
            return

        ligne, colonne, ancienne_valeur = self.historique.pop()
        e = self.entries[ligne][colonne]

        e.delete(0, tk.END)

        if ancienne_valeur != 0:
            e.insert(0, str(ancienne_valeur))
            e.config(fg="black")

        self.grille[ligne][colonne] = ancienne_valeur
        self.derniere_valeur[ligne][colonne] = (
            str(ancienne_valeur) if ancienne_valeur != 0 else None
        )

        self.highlight_selected(ligne, colonne)

    def remplir(self):
        for i in range(9):
            for j in range(9):
                val = self.grille[i][j]
                e = self.entries[i][j]

                e.delete(0, tk.END)

                if val != 0:
                    e.insert(0, str(val))
                    e.config(
                        state="disabled",
                        disabledforeground="black",
                        disabledbackground=self.base_colors[i][j]
                    )
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
        frame = tk.Frame(self, bg="lightyellow")

        tk.Label(
            frame,
            text="Choisis la difficulté",
            font=("Arial", 50),
            fg="lightblue",
            bg="lightyellow"
        ).grid(row=0, column=0, padx=20, pady=20)

        tk.Button(
            frame, text="Facile", font=("Arial", 30),
            command=lambda: self.lancer_jeu("Facile")
        ).grid(row=1, column=0, pady=10)

        tk.Button(
            frame, text="Moyen", font=("Arial", 30),
            command=lambda: self.lancer_jeu("Moyen")
        ).grid(row=2, column=0, pady=10)

        tk.Button(
            frame, text="Difficile", font=("Arial", 30),
            command=lambda: self.lancer_jeu("Difficile")
        ).grid(row=3, column=0, pady=10)

        self.changer_frame(frame)

    def get_nb_cases(self, difficulte):
        return {"Facile": 30, "Moyen": 40}.get(difficulte, 50)

    def lancer_jeu(self, difficulte):
        frame = tk.Frame(self, bg="lightyellow")

        grille = générer_grille()
        sudoku(grille)

        nb = self.get_nb_cases(difficulte)
        efface(grille, nb)

        ui = SudokuUI(frame, grille)
        ui.pack()

        tk.Button(
            frame, text="Annuler",
            command=ui.annuler
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            frame,
            text="Retour au menu",
            command=lambda: [setattr(ui, 'chrono_actif', False),
                             self.afficher_menu()]
        ).pack(side="left", padx=10, pady=10)

        self.changer_frame(frame)


app = App()
app.mainloop()
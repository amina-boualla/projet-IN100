# main.py
import tkinter as tk
from logique import generer_grille, sudoku, efface
from interface import SudokuUI


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
        frame.pack(fill = "both" , expand = True )

        tk.Label(
            frame,
            text="Choisis la difficulte",
            font=("Arial", 50),
            fg="lightblue",
            bg="lightyellow"
        ).grid(row=0, column=0, padx=20, pady=20)

        tk.Button(
            frame,
            text="Facile",
            font=("Arial", 30),
            command=lambda: self.lancer_jeu("Facile")
        ).grid(row=1, column=0, pady=10)

        tk.Button(
            frame,
            text="Moyen",
            font=("Arial", 30),
            command=lambda: self.lancer_jeu("Moyen")
        ).grid(row=2, column=0, pady=10)

        tk.Button(
            frame,
            text="Difficile",
            font=("Arial", 30),
            command=lambda: self.lancer_jeu("Difficile")
        ).grid(row=3, column=0, pady=10)

        self.changer_frame(frame)

    def get_nb_cases(self, difficulte):
        return {"Facile": 30, "Moyen": 40}.get(difficulte, 50)

    def lancer_jeu(self, difficulte):
        frame = tk.Frame(self, bg="lightyellow")

        solution  = generer_grille()
        sudoku(solution)

        grille = [row[:] for row in solution]

        nb = self.get_nb_cases(difficulte)
        efface(grille, nb)

        ui = SudokuUI(frame, grille, solution)
        ui.pack()


        tk.Button(
            frame,
            text="Annuler",
            command=ui.annuler
        ).pack(side="left", padx=10, pady=10)

        tk.Button(
            frame, 
            text = "Indice",
            command=ui.indice
        ).pack(side ="left" , padx = 10 , pady = 10)

        tk.Button(
            frame,
            text="Retour au menu",
            command=lambda: [
                setattr(ui, 'chrono_actif', False),
                self.afficher_menu()
            ]
        ).pack(side="left", padx=10, pady=10)

        self.changer_frame(frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()

import random
import tkinter as tk

class SudokuUI(tk.Frame):
    def __init__(self, parent, grille):
        super().__init__(parent)
        self.grille = grille
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


root = tk.Tk()

root.title("Sudoku")

ui = SudokuUI(root, grille)
ui.pack(padx=10, pady=10)

root.mainloop()

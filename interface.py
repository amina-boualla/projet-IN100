# interface.py
import tkinter as tk
from logique import valide_ou_pas


# ── Fonctions greffées sur SudokuUI ────────────────────────────────────────────

def create_barre_nombres(self):
    frame = tk.Frame(self)
    frame.grid(row=4, column=0, columnspan=3, pady=10)

    self.boutons_nombres = {}
    self.nombre_selectionne = None

    for i in range(1, 10):
        btn = tk.Button(
            frame,
            text=str(i),
            font=("Arial", 16),
            width=3,
            command=lambda n=i: self.selectionner_nombre(n)
        )
        btn.grid(row=0, column=i - 1, padx=5)
        self.boutons_nombres[i] = btn


def selectionner_nombre(self, nombre):
    self.nombre_selectionne = nombre

    for n in self.boutons_nombres:
        self.boutons_nombres[n].config(bg="SystemButtonFace")

    self.boutons_nombres[nombre].config(bg="lightblue")

    self.highlight_meme_nombre(nombre)


def highlight_meme_nombre(self, nombre):
    """Colorie en bleu clair toutes les cases contenant le chiffre sélectionné."""
    self.reset_colors()

    for i in range(9):
        for j in range(9):
            val = self.entries[i][j].get()
            if val == str(nombre):
                self.set_bg(i, j, "#cce6ff")


def cliquer_case(self, ligne, colonne):
    e = self.entries[ligne][colonne]

    if e.cget("state") == "disabled":
        self.highlight_selected(ligne, colonne)
        return

    self.highlight_selected(ligne, colonne)

    if self.nombre_selectionne is not None:
        e.delete(0, tk.END)
        e.insert(0, str(self.nombre_selectionne))

        self.verifier_case(
            type("Event", (), {"keysym": None}),
            ligne,
            colonne
        )


def update_barre_nombres(self):
    counts = self.compter_nombres()

    for num in range(1, 10):
        btn = self.boutons_nombres[num]

        if counts[num] >= 9:
            btn.config(state="disabled", fg="gray")
        else:
            btn.config(state="normal", fg="black")


# ── Classe principale ───────────────────────────────────────────────────────────

class SudokuUI(tk.Frame):
    def __init__(self, parent, grille , solution):
        super().__init__(parent)
        self.grille = grille
        self.solution = solution 
        self.entries = [[None]*9 for _ in range(9)]
        self.base_colors = [[None]*9 for _ in range(9)]
        self.secondes = 0
        self.chrono_label = None
        self.chrono_actif = True
        self.derniere_valeur = [[None]*9 for _ in range(9)]
        self.historique = []
        self.indices_restants = 9
        self.label_indices = None
        self.indices_utilises = set()
        self.case_selectionnee = None

        self.erreurs = 0
        self.label_erreurs = None

        self.create_bandeau()
        self.create_grid()
        create_barre_nombres(self)
        self.remplir()

    def compter_nombres(self):
        counts = {i: 0 for i in range(1, 10)}

        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if val.isdigit():
                    counts[int(val)] += 1

        return counts

    def create_bandeau(self):
        bandeau = tk.Frame(self, bg="lightyellow")
        bandeau.grid(row=0, column=0, columnspan=3, pady=(0, 8))

        self.chrono_label = tk.Label(
            bandeau,
            text="Temps : 00:00",
            font=("Arial", 14),
            bg="lightyellow"
        )
        self.chrono_label.pack(side="left", padx=20)

        self.label_erreurs = tk.Label(
            bandeau,
            text="Erreurs : 0/3",
            font=("Arial", 14),
            bg="lightyellow",
            fg="red"
        )
        self.label_erreurs.pack(side="left", padx=20)

        self.update_chrono()

        self.label_indices = tk.Label(
            bandeau,
            text="Indices : 9/9",
            font=("Arial", 14),
            bg="lightyellow",
            fg="blue"
        )
        self.label_indices.pack(side="left", padx=20)

    def update_chrono(self):
        if self.chrono_actif:
            self.secondes += 1
            minutes = self.secondes // 60
            secondes = self.secondes % 60

            self.chrono_label.config(
                text=f"Temps : {minutes:02d}:{secondes:02d}"
            )

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
                            lambda event, l=ligne, c=colonne:
                            self.verifier_case(event, l, c)
                        )

                        entry.bind(
                            "<Button-1>",
                            lambda event, l=ligne, c=colonne:
                            self.cliquer_case(l, c)
                        )

    def ajouter_erreur(self):
        self.erreurs += 1
        self.label_erreurs.config(text=f"Erreurs : {self.erreurs}/3")

        if self.erreurs >= 3:
            self.perdu()

    def perdu(self):
        self.chrono_actif = False

        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state="disabled")

        popup = tk.Toplevel(self)
        popup.title("Perdu")

        tk.Label(
            popup,
            text="Game over",
            font=("Arial", 20)
        ).pack(padx=20, pady=20)

        tk.Button(
            popup,
            text="OK",
            command=popup.destroy
        ).pack(pady=10)

    def verifier_victoire(self):
        """Vérifie si la grille est entièrement et correctement remplie."""
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                if not val.isdigit():
                    return False
                if self.entries[i][j].cget("fg") == "red":
                    return False
        return True

    def gagner(self):
        """Affiche l'écran de victoire."""
        self.chrono_actif = False

        minutes = self.secondes // 60
        secondes = self.secondes % 60

        indices_utilises = 9 - self.indices_restants
        
        for i in range(9):
            for j in range(9):
                self.set_bg(i, j, "#90ee90")

        popup = tk.Toplevel(self)
        popup.title("Bravo !")
        popup.configure(bg="lightyellow")

        tk.Label(
            popup,
            text="🎉 Félicitations !",
            font=("Arial", 26, "bold"),
            fg="#2e7d32",
            bg="lightyellow"
        ).pack(padx=30, pady=(20, 5))

        tk.Label(
            popup,
            text="Tu as résolu le Sudoku !",
            font=("Arial", 16),
            bg="lightyellow"
        ).pack(padx=30)

        tk.Label(
            popup,
            text=f"Temps : {minutes:02d}:{secondes:02d}",
            font=("Arial", 16),
            bg="lightyellow",
            fg="#1565c0"
        ).pack(padx=30, pady=5)

        tk.Label(
            popup,
            text=f"Erreurs : {self.erreurs}/3",
            font=("Arial", 14),
            bg="lightyellow",
            fg="red"
        ).pack(padx=30)

        tk.Label(
            popup,
            text = f"Indices utilisés : {indices_utilises}/9",
            font=("Arial", 14),
            bg="lightyellow",
            fg = "green"
        ).pack(pady=5)

        tk.Button(
            popup,
            text="OK",
            font=("Arial", 14),
            command=popup.destroy
        ).pack(pady=20)



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
        self.case_selectionnee = (ligne , colonne)

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
            self.update_barre_nombres()
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
            self.ajouter_erreur()

        self.grille[ligne][colonne] = val
        self.update_barre_nombres()

        if self.verifier_victoire():
            self.after(200, self.gagner)

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
        self.update_barre_nombres()

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

        self.update_barre_nombres()

    def indice(self):
        if self.indices_restants == 0:
            self.label_indices.config(text="Indices : 0/9 ")
            return

        if not hasattr(self, "case_selectionnee"):
            return

        i, j = self.case_selectionnee

    # si déjà remplie
        if self.grille[i][j] != 0:
            return

        valeur = self.solution[i][j]

        self.entries[i][j].delete(0, tk.END)
        self.entries[i][j].insert(0, str(valeur))

        self.grille[i][j] = valeur

        self.indices_restants -= 1

        self.label_indices.config(
            text=f"Indices : {self.indices_restants}/9"
        )

# Greffage des méthodes externes sur la classe
SudokuUI.selectionner_nombre = selectionner_nombre
SudokuUI.highlight_meme_nombre = highlight_meme_nombre
SudokuUI.cliquer_case = cliquer_case
SudokuUI.update_barre_nombres = update_barre_nombres

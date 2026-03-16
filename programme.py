
import random

def générer_grille():
  grille = [[0]*9 for _ in range(9)]
  return grille

def valide_ou_pas(grille, ligne, colonne, numéro):
    if numéro in grille[ligne]:
        return False
    if numéro in [grille[l][colonne] for l in range(9)]: #https://professeurb.github.io/articles/sudoku/ utilisation du code, pour la division par cases et le fait d'avoir bien des colonnes
        return False
    case_ligne = 3 * (ligne // 3) # donne la première sous case de chaque case de 3x3
    case_colonne = 3 * (colonne // 3)
    for l in range(case_ligne, case_ligne + 3):
        for c in range(case_colonne, case_colonne + 3):
            if grille[l][c] == numéro:
                return False
    return True

def sudoku(grille):
    for ligne in range(9):
        for colonne in range(9):
            if grille[ligne][colonne] == 0:
                for numéro in range(1,10):
                    if valide_ou_pas(grille, ligne, colonne, numéro):
                        grille[ligne][colonne] = numéro
                        if sudoku(grille):
                            return True
                        grille[ligne][colonne] = 0
                return False
    return True

def efface(grille, n):
    while n > 0:
        ligne = random.randint(0, 8)
        colonne = random.randint(0, 8)

        if grille[ligne][colonne] != 0:
            grille[ligne][colonne] = 0
            n -= 1

    return grille

grille = générer_grille()

sudoku(grille)

for ligne in grille:
    print(ligne)

print(efface(grille, 50))
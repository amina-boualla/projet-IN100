# logique.py
import random


def generer_grille():
    grille = [[0]*9 for _ in range(9)]
    return grille


def valide_ou_pas(grille, ligne, colonne, numero):
    if numero in grille[ligne]:
        return False
    if numero in [grille[l][colonne] for l in range(9)]:
        return False

    case_ligne = 3 * (ligne // 3)
    case_colonne = 3 * (colonne // 3)

    for l in range(case_ligne, case_ligne + 3):
        for c in range(case_colonne, case_colonne + 3):
            if grille[l][c] == numero:
                return False

    return True


def sudoku(grille):
    for ligne in range(9):
        for colonne in range(9):
            if grille[ligne][colonne] == 0:
                nombres = list(range(1, 10))
                random.shuffle(nombres)

                for numero in nombres:
                    if valide_ou_pas(grille, ligne, colonne, numero):
                        grille[ligne][colonne] = numero

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

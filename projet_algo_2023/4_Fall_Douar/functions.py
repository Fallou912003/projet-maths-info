import time
import sys
import signal
import tkinter as tk
import copy


#-----------------------------------------------------------------------------------------
#pour déterminer s'il y a une case blanche dans un bloc
def est_blanche(l) :
    if l == [] :
        return False
    if l[0] == 0 :
        return True
    else :
        return est_blanche(l[1:])


#-----------------------------------------------------------------------------------------
#pour déterminer s'il y a une case noire dans un bloc
def est_noire(l) :
    if l == [] :
        return False
    if l[0] == 1 :
        return True
    else :
        return est_noire(l[1:])


#-----------------------------------------------------------------------------------------
#calcule la transposée de la matrice
def transposee(matrice) :
    tmatrice = [[ligne[i] for ligne in matrice] for i in range(len(matrice[0]))]
    return tmatrice


#-----------------------------------------------------------------------------------------
#transforme les fichiers instances en séquences de lignes et de colonnes et retourne aussi la grille non coloriée
def fichier_a_sequence(nom_fichier):
    lignes = []
    colonnes = []

    with open(nom_fichier, 'r') as fichier:
        colonnes_commencees = False

        for ligne in fichier:
            ligne = ligne.strip()

            if not colonnes_commencees:
                if ligne == '#':
                    colonnes_commencees = True
                else:
                    valeurs = [int(x) for x in ligne.split()]
                    lignes.append(valeurs if valeurs else [])
            else:
                valeurs = [int(x) for x in ligne.split()]
                colonnes.append(valeurs if valeurs else [])

    nb_lignes = len(lignes)
    nb_colonnes = len(colonnes)

    # Initialisation de la matrice A avec des -1 comme les cases non coloriées
    A = [[-1] * nb_colonnes for _ in range(nb_lignes)]

    return lignes, colonnes, A


#-----------------------------------------------------------------------------------------
#permet d'afficher la grille sur le terminal
def print_coloriage(A):
    for row in A:
        for cell in row:
            if cell == 0:
                print("◻️", end=" ") 
            elif cell == 1:
                print("◼️", end=" ") 
            else:
                print("?", end=" ") 
        print()


#-----------------------------------------------------------------------------------------
#teste si la grille (sous forme de matrice) est entièrement coloriée ou pas
def test_matrice_coloree(A):
    ok = True
    for i in range(len(A)) :
        for j in range(len(A[0])) :
            if A[i][j] == -1 :
                return not ok
            else :
                ok = True
    return ok


#-----------------------------------------------------------------------------------------
#permet d'afficher la grille obtenue dans un fichier crée dans le meme répertoire
def print_coloriage_to_file(A, filename):
    with open(filename, 'w') as f:
        for row in A:
            for cell in row:
                if cell == 0:
                    f.write("◻️ ")
                elif cell == 1:
                    f.write("◼️ ")
                else:
                    f.write("? ")
            f.write("\n")
    

#-----------------------------------------------------------------------------------------
#permet d'afficher la grille obtenue sous forme d'image nette
def affichage_coloriage(A):
    
    fenetre = tk.Tk()
    fenetre.title("Coloriage")

    Canvas = tk.Canvas(fenetre, width=len(A[0]) * 10, height=len(A) * 10)
    Canvas.pack()

    taille_case = 10

    for i, row in enumerate(A):
        for j, cell in enumerate(row):
            x1, y1 = j * taille_case, i * taille_case
            x2, y2 = x1 + taille_case, y1 + taille_case

            if cell == 0:
                Canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            elif cell == 1:
                Canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")

    fenetre.mainloop()

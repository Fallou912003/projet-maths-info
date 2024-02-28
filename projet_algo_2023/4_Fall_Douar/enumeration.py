#---------------------------------------------la partie 1-2------------------------------------------------#
# Projet Fall et Douar
# Pour la matrice en parametre quand les cases valent 1 alors elles sont de couleur noire, si elles valent 0 alors elles sont 
# blanches et incolores quand elles valent -1

import time
import sys
import signal
import tkinter as tk
import copy

#-------------------------------------------------------------------------------------------
#pour déterminer s'il y a une case blanche dans un bloc
def est_blanche(l) :
    if l == [] :
        return False
    if l[0] == 0 :
        return True
    else :
        return est_blanche(l[1:])
    
#-------------------------------------------------------------------------------------------
#pour déterminer s'il y a une case noire dans un bloc
def est_noire(l) :
    if l == [] :
        return False
    if l[0] == 1 :
        return True
    else :
        return est_noire(l[1:])


#-------------------------------------------------------------------------------------------
#fonnction qui calcule les T(j,l) codé en programmation dynamique avec les différents cas évoqués dans le rapport
def T(j,l,i,s,m,memo):
    if l == 0:
        return not(est_noire(m[i][:j+1]))

    if (j,l,i) in memo:
        return memo[(j,l,i)]
    
    else : 
        if j < s[l-1] - 1:
            memo[(j,l,i)] = False
        elif j == s[l-1] - 1:
            if l == 1:
                memo[(j,l,i)] = not(est_blanche(m[i][:j+1]))
            else:
                memo[(j,l,i)] = False
        else:
            if m[i][j] == 0:
                memo[(j,l,i)] = T(j-1,l,i,s,m,memo)
            elif m[i][j] == 1:
                memo[(j,l,i)] = (m[i][j-s[l-1]] != 1 and \
                                not(est_blanche(m[i][j-s[l-1]+1:j])) and \
                                T(j-s[l-1]-1,l-1,i,s,m,memo))
            else:
                memo[(j,l,i)] = (T(j-1,l,i,s,m,memo) or \
                               (T(j-s[l-1]-1,l-1,i,s,m,memo) and \
                               not(est_blanche(m[i][j-s[l-1]+1:j])) and \
                               (m[i][j-s[l-1]] != 1 if j-s[l-1] != 0 or l != 1 else True)))

    return memo[(j,l,i)]


#------------------------------------------------------------------------------------------
#permet de voir si on peut colorer une ligne avec la séquence s et la colore selon les différents tests possibles
#si case est coloriée on teste si la coloriage est valide ou pas
def coloreLigne(A,i,s) :
    A_prime = copy.deepcopy(A)
    M = len(A_prime[i])
    colonne_a_voir = set()
    ok = True

    for j in range(M) :
        if A_prime[i][j] == -1 :
            test_blanche = False
            test_noire = False

            A_prime[i][j] = 0
            if T(M-1,len(s),i,s,A_prime,{}) :
                test_blanche = True
                A_prime[i][j] = 1
            else:
                A_prime[i][j] = 1

            if T(M-1,len(s),i,s,A_prime,{}) :
                test_noire = True
                A_prime[i][j] = -1
            else :
                A_prime[i][j] = -1

            if test_blanche == False and test_noire == False :
                A_prime[i][j] = -1
                ok = False
                return ok, A_prime, colonne_a_voir
            elif test_blanche == False and test_noire == True :
                A_prime[i][j] = 1
                ok = True
                colonne_a_voir.add(j)
            elif test_blanche == True and test_noire == False :
                A_prime[i][j] = 0
                ok = True
                colonne_a_voir.add(j)
            else :
                A_prime[i][j] = -1
                ok = True
        else :
            if not T(M-1,len(s),i,s,A_prime,{}):
                ok = False
                return ok, A_prime, colonne_a_voir
            ok = True

    return ok, A_prime, colonne_a_voir
                

#-----------------------------------------------------------------------------------------
#calcule la transposée de la matrice
def transposee(matrice) :
    tmatrice = [[ligne[i] for ligne in matrice] for i in range(len(matrice[0]))]
    return tmatrice


#-------------------------------------------------------------------------------------------
#permet de voir si on peut colorer une ligne avec la séquence s et la colore selon les différents tests possibles
#si case est coloriée on teste si la coloriage est valide ou pas
def coloreColonne(A,j,s) :
    A_prime = transposee(A)
    N = len(A_prime[j])
    ligne_a_voir = set()
    ok = True

    for i in range(N) :
        if A_prime[j][i] == -1 :
            test_blanche = False
            test_noire = False

            A_prime[j][i] = 0
            if T(N-1,len(s),j,s,A_prime,{}) :
                test_blanche = True
                A_prime[j][i] = 1
            else:
                A_prime[j][i] = 1

            if T(N-1,len(s),j,s,A_prime,{}) :
                test_noire = True
                A_prime[j][i] = -1
            else :
                A_prime[j][i] = -1

            if test_blanche == False and test_noire == False :
                A_prime[j][i] = -1
                ok = False
                A_prime = transposee(A_prime)
                return ok, A_prime, ligne_a_voir
            elif test_blanche == False and test_noire == True :
                A_prime[j][i] = 1
                ok = True
                ligne_a_voir.add(i)
            elif test_blanche == True and test_noire == False :
                A_prime[j][i] = 0
                ok = True
                ligne_a_voir.add(i)
            else :
                A_prime[j][i] = -1
                ok = True
        else :
            if not T(N-1,len(s),j,s,A_prime,{}) :
                ok = False
                A_prime = transposee(A_prime)
                return ok, A_prime, ligne_a_voir
            ok = True
    A_prime = transposee(A_prime)
    return ok, A_prime, ligne_a_voir
                

#-------------------------------------------------------------------------------------------
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

    # Initialisation de la matrice A avec des -1 comme des indéterminés
    A = [[-1] * nb_colonnes for _ in range(nb_lignes)]

    return lignes, colonnes, A


#-------------------------------------------------------------------------------------------
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


#-------------------------------------------------------------------------------------------
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


#-------------------------------------------------------------------------------------------
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
    

#-------------------------------------------------------------------------------------------
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


#-------------------------------------------------------------------------------------------
#on met filename pour écrire le résultat de la grille dans un fichier
#permet de faire la coloration partielle ou totale d'une grille. Elle est codée à partir du pseudo-code du sujet
def coloration(A,lignes_sequences,colonnes_sequences):
    A_prime = copy.deepcopy(A)
    lignes_a_voir = set(range(len(A_prime)))
    colonnes_a_voir = set(range(len(A_prime[0])))

    while lignes_a_voir or colonnes_a_voir:
        for i in lignes_a_voir.copy():
            ok, A_prime, nouvelles_colonnes = coloreLigne(A_prime, i, lignes_sequences[i])
        
            if not ok:
                return "False", []
            colonnes_a_voir.update(nouvelles_colonnes)
            lignes_a_voir.remove(i)

        for j in colonnes_a_voir.copy():
            ok, A_prime, nouvelles_lignes = coloreColonne(A_prime, j, colonnes_sequences[j])
            if not ok:
                return "False", []
            lignes_a_voir.update(nouvelles_lignes)
            colonnes_a_voir.remove(j)

    if test_matrice_coloree(A_prime) :
        return "vrai", A_prime

    return "NeSaitPas", A_prime


#-------------------------------------------------------------------------------------------
#permet de colorier une case d'une grille et colore les autres cases à partir de ceux déjà coloriées
#si la grille est déjà coloriée elle retourne vrai
#si la case courante est déjà coloriée alors on passe à d'autres cas en retournant NeSaitPas
#sinon on colorie les cases avec c et on applique le même algo que coloration avec quelques modifications
def ColorierEtPropager(A,i,j,c,lignes_sequences,colonnes_sequences):

    A_prime = copy.deepcopy(A) 

    if test_matrice_coloree(A_prime) :
            return "vrai", A_prime
    
    if A_prime[i][j] != -1 :
        return "NeSaitPas", A_prime
    
    if c == "noire" :
        A_prime[i][j] = 1
    else : 
        A_prime[i][j] = 0
    
    
    if test_matrice_coloree(A_prime) :
        return "vrai", A_prime
        
    lignes_a_voir = {i}
    colonnes_a_voir = {j}

    while lignes_a_voir or colonnes_a_voir:
        for i in lignes_a_voir.copy():

            ok, A_prime, nouvelles_colonnes = coloreLigne(A_prime, i, lignes_sequences[i])
        
            if not ok:
                return "False", []
            colonnes_a_voir.update(nouvelles_colonnes)
            lignes_a_voir.remove(i)

        for j in colonnes_a_voir.copy():
            
            ok, A_prime, nouvelles_lignes = coloreColonne(A_prime, j, colonnes_sequences[j])
            if not ok:
                return "False", []
            lignes_a_voir.update(nouvelles_lignes)
            colonnes_a_voir.remove(j)

    if test_matrice_coloree(A_prime) :
        return "vrai", A_prime

    return "NeSaitPas", A_prime


#-------------------------------------------------------------------------------------------
#on applique ici le pseudo-code donné dans le sujet
#on ajoute filename dans les paramètres afin de pouvoir si on le choisit dessiner la grille dans un fichier du même répertoire
#on ajoute aussi choix_affichage afin de pouvoir afficher selon le choix de l'utilisateur la grille dans le terminal, dans un fichier ou sous forme d'image
def enumeration_rec(A,k,c,lignes_sequences,colonnes_sequences,filename,choix_affichage) :

    N = len(lignes_sequences)
    M = len(colonnes_sequences)

    if k == N * M :
        if choix_affichage == 0 :
            print_coloriage(A)
        elif choix_affichage == 1:
            affichage_coloriage(A)
        else :
            print_coloriage_to_file(A, filename)
        return True
    
    i = k // M
    j = k % M
    ok, A_prime = ColorierEtPropager(A,i,j,c,lignes_sequences,colonnes_sequences)

    if ok == "False" :
        return False
    elif ok == "vrai" :
        if choix_affichage == 0 :
            print_coloriage(A_prime)
        elif choix_affichage == 1:
            affichage_coloriage(A_prime)
        else :
            print_coloriage_to_file(A_prime, filename)
        return True
    
    k_prime = k + 1
    i = k_prime // M
    j = k_prime % M
    while A_prime[i][j] != -1 :
        k_prime = k_prime + 1
        i = k_prime // M
        j = k_prime % M 
    
    A_seconde = copy.deepcopy(A_prime)

    return (enumeration_rec(A_seconde, k_prime, "blanche", lignes_sequences, colonnes_sequences,filename,choix_affichage)) or \
        (enumeration_rec(A_seconde, k_prime, "noire", lignes_sequences, colonnes_sequences, filename,choix_affichage))


#-------------------------------------------------------------------------------------------
#fonction implémenté à l'aide du pseudo-code du sujet
def enumeration(A,lignes_sequences,colonnes_sequences,filename,choix_affichage) :
    
    ok, A_prime = coloration(A,lignes_sequences,colonnes_sequences)

    if ok == "False" :
        return False
    
    return (enumeration_rec(A_prime, 0, "blanche", lignes_sequences, colonnes_sequences, filename, choix_affichage)) or \
        (enumeration_rec(A_prime, 0, "noire", lignes_sequences, colonnes_sequences, filename, choix_affichage))






#------------------------------------------TESTS---------------------------------------#


#fonction pour le timeout de 2 mn
def handler(signum, frame):
    print("Timeout! L'exécution a pris trop de temps.")
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)
timeout_seconds = 1000
signal.alarm(timeout_seconds)

#demande à l'utilisateur de choisir s'il veut tester une instance particulièrement ou toutes les instances
choix = int(input("Tapez 0 pour afficher la grille coloriée de l'instance choisie ou tapez 1 pour afficher la grille de toutes les instances :"))

if choix == 1 :
    try:
        #on change de nom de fichier à chaque tour de boucle
        nom_fichier_base = "0.txt"
        nom_fichier_resultat = "resultat_0.txt"
        choix_affichage = int(input("Tapez 0 pour afficher le coloriage sur le terminal, 1 pour l'afficher en pixels ou 2 pour l'afficher dans un fichier :"))

        for i in range(17):
            
            #recupère les listes de séquences de lignes et de colonnes dans le fichier courant
            nom_fichier = nom_fichier_base.replace("0", str(i))
            lignes_sequences, colonnes_sequences, grille_non_coloree = fichier_a_sequence(nom_fichier)

            # écriture des instances #.txt dans les fichiers resultat_#.txt
            nom_fichier_res = nom_fichier_resultat.replace("0", str(i))
        
            #mesure du temps de calcul de la fonction
            debut = time.time()
            reponse = enumeration(grille_non_coloree, lignes_sequences, colonnes_sequences, nom_fichier_res, choix_affichage)
            fin = time.time()

            #regarde si la coloration est possible ou pas
            if not reponse :
                print("pas de solution possible pour cette instance : ", nom_fichier)
            else :
                print("Voici la solution à votre probleme : ", nom_fichier)

            #temps d'exécution de la fonction énumération
            temps = fin - debut
            print("Temps d'exécution :", temps, "secondes")

    #exeption levée si le temps d'exécution dépasse 2 mn ou pour une autre cas de figure
    except Exception as e:
        print(f"Une exception s'est produite : {e}")
    finally:
        signal.alarm(0)

else :
    #demande à l'utilisateur les requêtes suivantes
    choix_instance = input("Choisissez l'instance que vous voulez tester:")
    choix_affichage = int(input("Tapez 0 pour afficher le coloriage sur le terminal, 1 pour l'afficher en pixels ou 2 pour l'afficher dans un fichier :"))

    #permet de recupérer le fichier choisi
    nom_fichier = f"{choix_instance}.txt"
    nom_fichier_res = f"resultat_{choix_instance}.txt"
    lignes_sequences, colonnes_sequences, grille_non_coloree = fichier_a_sequence(nom_fichier)

    #mesure du temps de calcul de la fonction
    debut = time.time()
    reponse = enumeration(grille_non_coloree, lignes_sequences, colonnes_sequences, nom_fichier_res, choix_affichage)
    fin = time.time()

    #regarde si la coloration est possible ou pas
    if not reponse :
        print("pas de solution possible pour cette instance : ", nom_fichier)
    else :
        print("Voici la solution à votre probleme : ", nom_fichier)

    #donne le temps de calcul de coloration
    temps = fin - debut
    print("Temps d'exécution :", temps, "secondes")




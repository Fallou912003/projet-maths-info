""" Partie 1 : Méthode incomplète de résolution """
from functions import *

#-----------------------------------------------------------------------------------
#1.1
# Question 4 : Renvoie la valeur de T(j,l) pour la ligne i et pour la sequence s
def T1(j,l,i,s):
    if l == 0 :
        return True
    else:
        if j < s[l-1]-1 :
            return False
        elif j == s[l-1]-1 :
            if l == 1 :
                return True
            else :
                return False
        else :
            if (l==1 and  (j == s[0]-1)) : 
                return True 
            return T1(j-s[l-1]-1,l-1,i,s) or T1(j-1,l,i,s)
        

#-----------------------------------------------------------------------------------
#1.2
# Question 7 : construit le tableau T correspondant au vecteur V tel que T[j][l] = T(j,l) récursivement, \
# sachant que certaines cases peuvent être déjà coloriées en blanc ou en noir. Elle est implémentée par programmation dynamique \
# avec memoisation
def T2(j,l,i,s,m,memo):
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
                memo[(j,l,i)] = T2(j-1,l,i,s,m,memo)
            elif m[i][j] == 1:
                memo[(j,l,i)] = (m[i][j-s[l-1]] != 1 and \
                               not(est_blanche(m[i][j-s[l-1]+1:j])) and \
                               T2(j-s[l-1]-1,l-1,i,s,m,memo))
            else:
                memo[(j,l,i)] = (T2(j-1,l,i,s,m,memo) or \
                               (T2(j-s[l-1]-1,l-1,i,s,m,memo) and \
                               not(est_blanche(m[i][j-s[l-1]+1:j])) and \
                               (m[i][j-s[l-1]] != 1 if j-s[l-1] != 0 or l != 1 else True)))

    return memo[(j,l,i)]


#-----------------------------------------------------------------------------------
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
            if T2(M-1,len(s),i,s,A_prime,{}) :
                test_blanche = True
                A_prime[i][j] = 1
            else:
                A_prime[i][j] = 1

            if T2(M-1,len(s),i,s,A_prime,{}) :
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
            if not T2(M-1,len(s),i,s,A_prime,{}):
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
            if T2(N-1,len(s),j,s,A_prime,{}) :
                test_blanche = True
                A_prime[j][i] = 1
            else:
                A_prime[j][i] = 1

            if T2(N-1,len(s),j,s,A_prime,{}) :
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
            if not T2(N-1,len(s),j,s,A_prime,{}) :
                ok = False
                A_prime = transposee(A_prime)
                return ok, A_prime, ligne_a_voir
            ok = True
    A_prime = transposee(A_prime)
    return ok, A_prime, ligne_a_voir
                

#-----------------------------------------------------------------------------------
#permet de faire la coloration partielle ou totale d'une grille. Elle est codée à partir du pseudo-code du sujet
# le paramètre filename a été ajouté afin de pouvoir par choix créer un fichier dans laquelle on dessine la grille à l'intérieur
# le paramètre choix_affichage a été ajouté afin de pouvoir choisir le mode d'affichage : soit afficher la grille 
# obtenue dans le terminal , soit l'afficher sous forme d'image nette ou bien l'afficher dans un fichier
def coloration(A,lignes_sequences,colonnes_sequences,filename,choix_affichage):
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
        if choix_affichage == 0 :
            print_coloriage(A_prime)
        elif choix_affichage == 1:
            affichage_coloriage(A_prime)
        else :
            print_coloriage_to_file(A_prime, filename)
        return "vrai", A_prime

    
    if choix_affichage == 0 :
        print_coloriage(A_prime)
    elif choix_affichage == 1:
        affichage_coloriage(A_prime)
    else :
        print_coloriage_to_file(A_prime, filename)
    return "NeSaitPas", A_prime


#--------------------------------TESTS-------------------------------------#
#demande à l'utilisateur les requêtes suivantes
choix_instance = input("Choisissez l'instance que vous voulez tester :")
choix_affichage = int(input("Tapez 0 pour afficher le coloriage sur le terminal, 1 pour l'afficher en pixels ou 2 pour l'afficher dans un fichier :"))

#permet de recupérer le fichier choisi
nom_fichier = f"{choix_instance}.txt"
nom_fichier_res = f"resultat_{choix_instance}.txt"
lignes_sequences, colonnes_sequences, grille_non_coloree = fichier_a_sequence(nom_fichier)

#mesure du temps de calcul de la fonction
debut = time.time()
reponse = coloration(grille_non_coloree, lignes_sequences, colonnes_sequences, nom_fichier_res, choix_affichage)
fin = time.time()

#regarde si la coloration est possible ou pas
if not reponse :
    print("pas de solution possible pour cette instance : ", nom_fichier)
else :
    print("Voici la solution à votre probleme : ", nom_fichier)

#donne le temps de calcul de coloration
temps = fin - debut
print("Temps d'exécution :", temps, "secondes")




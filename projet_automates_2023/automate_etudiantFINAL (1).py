#!/usr/bin/env python
# coding: utf-8

# ---
# ## Sorbonne Université
# # <center> Mathématiques discrètes </center>
# ## <center> LU2IN005 </center>
# ## <div style="text-align:right;"> Année 2022-2023 </div>
# ---

# ---
# # <center> TME programmation d'automates finis </center>
# L'objectif de ce TME est de programmer en python quelques uns des
# algorithmes pour les automates finis vus en cours et en TD, en
# utilisant des structures de données fournies dans le code mis à votre
# disposition.
# ---
# # Consignes
# Copiez dans votre répertoire de travail les fichiers présents dans le Dossier 
# *Fichiers Python fournis* de la page Moodle de l'UE.
# 
# Ils contiennent les définitions de structures de données décrites
# ci-dessous, ainsi que des aide-mémoire sur l'utilisation de python.
# 
# **Le seul fichier que vous êtes autorisés à modifier** est celui-ci, c'est-à-dire
# `automate_etudiant.ipynb`, partiellement prérempli. 
# Les instructions `return` sont à supprimer lorsque
# vous remplirez le contenu des différentes fonctions.  Les autres
# fichiers n'ont pas besoin d'être lus (mais ils peuvent l'être).
# Si votre programme nécessite de lire des fichiers, **ceux-ci doivent être enregistrés dans le répertoire ExemplesAutomates** que vous avez téléchargé.
# ---

# _Binôme_
# ----------
# 
# **NOM**:      SRAIEB        
# 
# **Prénom**:       Siwar        
# 
# **Numéro d'étudiant**:     21114754
# 
# **NOM**:FALL
# 
# **Prénom**:   Serigne Fallou
# 
# **Numéro d'étudiant**: 21125890
# 
# 

# ### Table des matières
# 
# > [1. Présentation](#sec1)
# >> [1.1 La classe `State`](#sec1_1) <br>
# >> [1.2 La classe `Transition`](#sec1_2) <br>
# >> [1.3 La classe `Automate`](#sec1_3)
# 
# > [2. Prise en mains](#sec2)
# >> [2.1 Création d'automates](#sec2_1) <br>
# >> [2.2 Premières manipulations](#sec2_2) <br>
# 
# > [3. Exercices de base : tests et complétion](#sec3)
# 
# > [4. Déterminisation](#sec4)
# 
# > [5. Constructions sur les automates réalisant des opérations sur les langages acceptés](#sec5)
# >> [5.1 Opérations ensemblistes sur les langages](#sec5_1) <br>
# >> [5.2 Opérations rationnelles sur les langages](#sec5_2)

# In[69]:


## Import des bibliothèques nécessaires au projet.
## Ne pas modifier les fichiers "bibliothèque".

## Interpréter cette cellule avant de continuer.

from transition import *
from state import *
import os
import copy
from automateBase import AutomateBase

class Automate(AutomateBase):
    pass


# ### 1. Présentation  <a class="anchor" id="sec1"></a>
# 
# Le projet utilise le langage python avec une syntaxe légèrement
# différente de celle vue en **LU1IN001 / 011**, parce qu'il exploite en particulier
# la notion de classes d'objets. Une introduction à cette notion est présentée dans le livre associé
# au cours : cf [Chapitre 13](https://www-licence.ufr-info-p6.jussieu.fr/lmd/licence/2021/ue/LU1IN001-2021oct/cours2020.pdf).
# 
# De plus, le typage des variables est noté de façon légèrement différente, en commentaires, pour les déclarations
# comme pour les arguments des fonctions. Pour ces derniers, les types sont indiqués dans la première ligne de la documentation de la fonction.
# 
# Les particularités sont brièvement expliquées en annexe
# de ce document. Par ailleurs, vous trouverez dans la section
# `projet` de la page Moodle un mémo sur la syntaxe python, ainsi que la carte de
# référence du langage utilisée en **LU1IN001 / 011**.  On rappelle qu'une ligne
# commençant par `#` est un commentaire, ignoré par
# l'interpréteur.
# 
# Toutes les structures de données nécessaires à la construction des
# automates sont fournies sous la forme de classes python, pour les
# transitions d'un automate, ses états, et les automates
# eux-mêmes. Cette section indique comment les utiliser.

# #### 1.1 La classe `State` <a class="anchor" id="sec1_1"></a>
# 
# Un état est représenté par
# - un entier `id` (type `int`) qui définit son identifiant,
# - un booléen `init` (type `bool`) indiquant si c'est un état initial,
# - un booléen `fin` (type `bool`) indiquant si c'est un état final,
# - une chaîne de caractères `label` (type `str`) qui définit son étiquette, permettant de le *décorer*. Par défaut, cette variable est la version chaîne de caractères de l'identifiant de l'état. 
# 
# On définit l'alias de type `State` pour représenter les variables de ce type. 
# 
# Ainsi, l'instruction ci-dessous crée une variable `s` représentant un état d'identifiant `1`, qui est un état initial mais pas final, dont l'identifiant et l'étiquette  `1` :

# In[70]:


# s : State
s = State(1, True, False)


# Si l'on souhaite avoir une étiquette différente de l'identifiant, on
# utilise un quatrième argument :

# In[71]:


s = State(1, True, False, 'etat 1') 


# On accède ensuite aux différents champs de `s` par la notation pointée : exécutez les cellules suivantes pour observer l'affichage obtenu.

# In[72]:


print('La valeur de s.id est : ')
print(s.id)


# In[73]:


print('La valeur de s.init est : ')
print(s.init)


# In[74]:


print('La valeur de s.fin est : ')
print(s.fin)


# In[75]:


print('La valeur de s.label est : ')
print(s.label)


# In[76]:


print("L'affichage de s est : ")
print(s)


# Ainsi, une variable de type `State` est affichée par son étiquette et, entre parenthèses, si c'est un état initial et/ou final.

# #### 1.2 La classe `Transition` <a class="anchor" id="sec1_2"></a>
# 
# Une transition est représentée par 
# - un état `stateSrc` (type `State`) correspondant à son état de départ
# - un caractère `etiquette` (type `str`) donnant son   étiquette
# - un état `stateDest` (type `State`) correspondant à son état de destination
# 
# On définit l'alias de type `Transition` pour représenter les variables de ce type.
# 
# La séquence d'instructions suivante crée la transition d'étiquette `"a"` de l'état `s` (défini ci-dessus) vers lui-même et affiche les différents champs de la transition :

# In[77]:


# t : Transition
t = Transition(s, "a", s)


# In[78]:


print('La valeur de t.etiquette est : ')
print(t.etiquette)


# In[79]:


print("L'affichage de t.stateSrc est : ")
print(t.stateSrc)


# On remarque que la variable `stateSrc` est de type `State`, on obtient donc un état, et non uniquement un
# identifiant d'état. 

# In[80]:


print("L'affichage de t.stateDest est : ")
print(t.stateDest)


# In[81]:


print("L'affichage de t est : ")
print(t)


# #### 1.3 La classe `Automate` <a class="anchor" id="sec1_3"></a>
# 
# Un automate est représenté par
# - l'ensemble de ses transitions `allTransitions` (de type `set[Transition]`) 
# - l'ensemble de ses états `allStates` (de type `set[State]`)
# - une étiquette `label` (de type `str`) qui est éventuellement vide.
# 
# On définit l'alias de type `Automate` pour représenter les variables de ce type.
# 
# Ainsi, de même que pour les classes précédentes, l'accès aux
# différents champs se fait par la notation pointée. Par exemple, on
# obtient l'ensemble des états d'un automate `monAutomate` par
# l'instruction `monAutomate.allStates`.
# 
# Pour créer un automate, il existe trois possibilités.

# **Création à partir d'un ensemble de transitions.**<br>
# On peut d'abord utiliser le constructeur de signature `Automate : set[Transition] -> Automate`.<br>
# Il déduit alors l'ensemble des états à partir de l'ensemble des transitions et définit par défaut l'étiquette
# de l'automate comme la chaîne de caractères vide.
# 
# Par exemple, en commençant par créer les états et les transitions nécessaires :

# In[82]:


## création d'états
# s1 : State
s1 = State(1, True, False)
# s2 : State
s2 = State(2, False, True)

## création de transitions
# t1 : Transition
t1 = Transition(s1,"a",s1)
# t2 : Transition
t2 = Transition(s1,"a",s2)
# t3 : Transition
t3 = Transition(s1,"b",s2)
# t4 : Transition
t4 = Transition(s2,"a",s2)
# t5 : Transition
t5 = Transition(s2,"b",s2)
# set_transitions : set[Transition]
set_transitions = {t1, t2, t3, t4, t5}

## création de l'automate
# aut : Automate
aut = Automate(set_transitions)


# L'affichage de cet automate, par la commande `print(aut)` produit alors le résultat suivant : 

# In[83]:


print(aut)


# Les états de l'automate sont déduits de l'ensemble de transitions.
# 
# Optionnellement, on peut donner un nom à l'automate, en utilisant la variable `label`, par exemple :

# In[84]:


# aut2 : Automate
aut2 = Automate(set_transitions, label="A") 

print(aut2)


# **Création à partir d'un ensemble de transitions et d'un ensemble d'états.**<br>
# Dans le second cas, on crée un automate à partir d'un ensemble de
# transitions mais aussi d'un ensemble d'états, par exemple pour représenter des
# automates contenant des états isolés. Pour cela, on utilise le
# constructeur `Automate : set[Transition] x set[State] -> Automate`.
# 
# On peut également, optionnellement, donner un nom à l'automate :

# In[85]:


# set_etats : set[State]
set_etats = {s1, s2}

# aut3 : Automate
aut3 = Automate(set_transitions, set_etats, "B")

print(aut3)


# L'ordre des paramètres peut ne pas être respecté **à la condition** que l'on donne leur nom explicitement. Ainsi, la ligne suivante est correcte :

# In[86]:


aut = Automate(setStates = set_etats, label = "A", setTransitions = set_transitions)

print(aut)


# **Création à partir d'un fichier contenant sa description.**<br>
# La fonction `Automate.creationAutomate : str -> Automate` prend en argument un nom de fichier qui décrit un automate et construit l'automate correspondant (voir exemple ci-dessous).
# 
# La description textuelle de l'automate doit suivre le format suivant (voir exemple ci-dessous) :
# - #E: suivi de la liste des noms des états, séparés par
#   des espaces ou des passages à la ligne. Les noms d'états peuvent
#   être n'importe quelle chaîne alphanumérique pouvant également
#   contenir le symbole `_`. Par contre, si le nom d'état
#   contient des symboles *non numériques* il ne doit pas commencer
#   par un chiffre, sous peine de provoquer une erreur à l'affichage.
#   Ainsi, `10` et `A1` sont des noms d'états possibles,
#   mais `1A` ne l'est pas.
# - #I: suivi de la liste des états initiaux
#   séparés par des espaces ou des passages à la ligne, 
# - #F: suivi de la liste des
#   états finaux séparés par des espaces ou des passages à la ligne, 
# - #T: suivi de la liste des transitions séparées par des
#   espaces ou des passages à la ligne. Chaque transition est donnée
#   sous le format `(etat1, lettre, etat2)`.
# 
# Par exemple le fichier `exempleAutomate.txt` contenant <br>
# `#E: 0 1 2 3`<br>
# `#I: 0`<br>
# `#F: 3`<br>
# `#T: (0 a 0)`<br>
# `	(0 b 0)`<br>
# `	(0 a 1)`<br>
# `	(1 a 2)`<br>
# `	(2 a 3)`<br>
# `	(3 a 3)`<br>
# `	(3 b 3)`<br>
# est formaté correctement. L'appel suivant produira l'affichage...

# In[87]:


# automate : Automate
automate = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
print(automate)


# **Fonctions de manipulation des automates.**<br>
# La classe automate contient également de nombreuses fonctions utiles. Elles
# s'appliquent à un objet de type `Automate` et s'utilisent donc sous la forme
# `aut.<`*fonction*`>(<`*parametres*`>)` où `aut` est une variable de type `Automate`.
# 

# - `show : float -> NoneType` <br> 
#     prend en argument facultatif un flottant (facteur de grossissement, par défaut il vaut 1.0) et produit une représentation graphique de l'automate.<br>
#     Ainsi, en utilisant l'automate défini dans le fichier d'exemple précédent, l'instruction `automate.show(1.2)` produit l'image suivante :

# In[88]:


automate.show(1.2)


# - `addTransition : Transition -> bool`<br>
#   prend en argument une transition `t`, fait la mise à jour de
#   l'automate en lui ajoutant `t` et ajoute les états impliqués
#   dans l'automate s'ils en sont absents. Elle rend `True` si l'ajout a
#   eu lieu, `False` sinon (si `t` était déjà présente dans l'automate).
#   
# - `removeTransition : Transition -> bool`<br>
#   prend en argument une transition `t` et fait la mise à jour de
#   l'automate en lui enlevant la transition, sans modifier les
#   états. Elle rend `True` si la suppression a eu lieu, `False` sinon (si
#   `t` était absente de l'automate).
# 
# - `addState : State -> bool`<br>
#   prend en argument un état `s` et fait la mise à jour de
#   l'automate en lui ajoutant `s`.  Elle rend `True` si l'ajout a eu
#   lieu, `False` sinon (si `s` était déjà présent dans l'automate).
# 
# - `nextId : -> int`<br>
#   renvoie un entier id frais, en choisissant l'entier le plus petit,
#   strictement supérieur à tous les id des états de l'automate.
# 
# - `removeState : State -> bool`<br>
#   prend en argument un état `s` et fait la mise à jour de
#   l'automate en supprimant `s` ainsi que toutes ses transitions
#   entrantes et sortantes.  Elle rend `True` si l'ajout a eu lieu, `False`
#   sinon (si `s` était absent de l'automate).
#   
# - `getSetInitialStates :  -> set[State]`<br> 
#   rend l'ensemble des états initiaux.
# 
# - `getSetFinalStates :  -> set[State]`<br>
#   rend l'ensemble des états finaux.
# 
# - `getSetTransitionsFrom : State -> set[Transition]`<br>
#   rend l'ensemble des transitions sortant de l'état passé en argument.
# 
# - `prefixStates : int -> NoneType`<br>
#   modifie les identifiants et les étiquettes de tous les états de
#   l'automate en les préfixant par l'entier passé en argument.
# 
# - `succElem : State x str -> set[State]`<br>
#   étant donné un état `s` et un caractère `a`, elle rend l'ensemble des
#   états successeurs de `s` par le caractère `a`.  Formellement,
#   
#   $$succElem(s, a) = \{s' \in S \mid  s \xrightarrow{a} s'\}.$$
#   
#   Cet ensemble peut contenir plusieurs états si l'automate n'est pas déterministe.

# In[89]:


# Voilà le code de succElem

def succElem(self, state, lettre):
    """ State x str -> set[State]
        rend l'ensemble des états accessibles à partir d'un état state par l'étiquette lettre
    """
    successeurs = set()
    # t: Transitions
    for t in self.getSetTransitionsFrom(state):
        if t.etiquette == lettre:
            successeurs.add(t.stateDest)
    return successeurs

Automate.succElem = succElem


# Avec l'exemple précédent, on obtient :

# In[90]:


s0 = list(automate.getSetInitialStates())[0] ## on récupère l'état initial de automate
automate.succElem(s0, 'a')


# ### 2. Prise en mains  <a class="anchor" id="sec2"></a>
# 
# #### 2.1 Création d'automates <a class="anchor" id="sec2_1"></a>
# 
# Soit l'automate $\mathcal{A}$ défini sur l'alphabet $\{ a,b \}$, d'états $0,1,2$, 
# d'état initial 0, d'état final 2 et de transitions : <br>$(0,a,0)$, $(0,b,1)$, 
# $(1,a,2)$, $(1,b,2)$, $(2,a,0)$ et $(2,b,1)$.
# 
# 1. Créer l'automate $\mathcal{A}$ à l'aide de son ensemble de transitions. Pour cela, créer un état `s0`  
# d'identifiant $0$
#   qui soit initial, un état `s1` d'identifiant $1$ et un état
#   `s2` d'identifiant $2$ qui soit final. Puis créer `t1`, `t2`, `t3`, `t4`, `t5` et
#   `t6` les 6 transitions de l'automate. Créer enfin l'automate
#   `auto` à partir de ses transitions, par exemple avec l'appel<br>
#   `auto = Automate({t1,t2,t3,t4,t5,t6})`.<br>
#   Vérifier que l'automate correspond bien à $\mathcal{A}$ en l'affichant.

# In[91]:


# A faire 
## création d'états
# s0 : State
s0 = State(0, True, False)
# s1 : State
s1 = State(1, False, False)
# s2 : State
s2 = State(2, False, True)

## création de transitions
# t1 : Transition
t1 = Transition(s0,"a",s0)
# t2 : Transition
t2 = Transition(s0,"b",s1)
# t3 : Transition
t3 = Transition(s1,"a",s2)
# t4 : Transition
t4 = Transition(s1,"b",s2)
# t5 : Transition
t5 = Transition(s2,"a",s0)
# t6 : Transition
t6 = Transition(s2,"b",s1)
# set_transitions : set[Transition]
set_transitions = {t1, t2, t3, t4, t5, t6}

## création de l'automate
# aut : Automate
auto = Automate(set_transitions)
print(auto)
auto.show(1.2) 


# 2. Créer l'automate $\mathcal{A}$ à l'aide de sa liste de
#   transitions et d'états, par exemple à l'aide de l'appel<br>
#   `auto1 = Automate({t1,t2,t3,t4,t5,t6}, {s0,s1,s2})`<br>
#   puis afficher l'automate obtenu à l'aide de `print` puis à l'aide de `show`.
#   Vérifier que l'automate `auto1` est bien
#   identique à l'automate `auto`.

# In[92]:


# A faire 
# set_etats : set[State]
set_etats = {s0, s1, s2}

# aut3 : Automate
auto1 = Automate(set_transitions, set_etats)

print(auto1)
auto1.show(1.2)


# 3. Créer l'automate $\mathcal{A}$ à partir d'un fichier. Pour cela,
#   créer un fichier `auto2.txt`, dans lequel sont indiqués les
#   listes des états et des transitions, ainsi que l'état initial et
#   l'état final, en respectant la syntaxe donnée dans la section
#   précédente. Par exemple la liste d'états est décrite par la ligne
#   `#E: 0 1 2`.  Utiliser ensuite par exemple l'appel
#   `auto2 = Automate.creationAutomate("ExemplesAutomates/auto2.txt")`, puis afficher
#   l'automate `auto2` à l'aide de `print` ainsi qu'à l'aide de `show`.

# In[93]:


# A faire
auto2 = Automate.creationAutomate("ExemplesAutomates/auto2.txt")
print(auto2)
auto2.show(1.2)


# #### 2.2 Premières manipulations <a class="anchor" id="sec2_2"></a>
# 
# 1. Appeler la fonction `removeTransition` sur l'automate
#   `auto` en lui donnant en argument la transition $(0,a,1)$. Il
#   s'agit donc de créer une variable `t` de type
#   `Transition` représentant $(0,a,1)$ et d'effectuer l'appel
#   `auto.removeTransition(t)`. Observer le résultat sur un
#   affichage.  Appeler ensuite cette fonction sur `auto` en lui
#   donnant en argument la transition `t1`. Observer le résultat
#   sur un affichage. Appeler la fonction `addTransition` sur
#   l'automate `auto` en lui donnant en argument la transition
#   `t1`. Vérifier que l'automate obtenu est bien le même
#   qu'initialement.

# In[94]:


# A faire
t = Transition(0,"a",0)
auto.removeTransition(t)
print(auto)
auto.show(1.2)


# In[95]:


# A faire 
auto.removeTransition(t1)
print(auto)
auto.show(1.2)


# 2. Appeler la fonction `removeState` sur l'automate
#   `auto` en lui donnant en argument l'état
#   `s1`. Observer le résultat. Appeler la fonction
#   `addState` sur l'automate `auto` en lui donnant en
#   argument l'état `s1`. Créer un état `s0bis` d'identifiant
#   $0$ et initial. Appeler la fonction `addState` sur
#   `auto` avec `s0bis` comme argument. Observer le résultat.

# In[96]:


auto.addTransition(t1)
print(auto)
auto.show(1.2)


# 3. Appeler la fonction `getSetTransitionsFrom` sur
#   l'automate `auto1` avec `s1` comme argument. Afficher
#   le résultat.

# In[97]:


# A faire 
auto.removeState(s1)
print(auto)
auto.show(1.2)


# In[98]:


auto.addState(s1)
auto.show(1.2)


# In[99]:


s0bis = State(0, True, False)
auto.addState(s1)


# In[100]:


auto1.getSetTransitionsFrom(s1)


# ### 3. Exercices de base : tests et complétion  <a class="anchor" id="sec3"></a>

# 1. Donner une définition de la fonction `succ`
#   qui, étant donné un ensemble d'états $S$ et une chaîne de caractères
#       $a$ (de longueur 1), renvoie l'ensemble des états successeurs de tous les états de $L$ par le caractère $a$. Cette fonction doit généraliser la fonction `succElem` pour qu'elle prenne en paramètre un ensemble d'états au lieu d'un seul état.  Formellement, si $S$ est un ensemble d'états et $a$ une lettre,
#   $$succ(S,a) = \bigcup_{s \in S}succ(s,a) = \{s' \in S \mid \mbox{il
#     existe } s \in L \mbox{ tel que } s \xrightarrow{a} s'\}.$$

# In[101]:


# Voilà le code de succElem

def succ(self, setStates, lettre):
    successeurs = set()
    # t: Transitions
    for s in setStates:
        for t in self.getSetTransitionsFrom(s):
            if t.etiquette == lettre:
                successeurs.add(t.stateDest)
    return successeurs

Automate.succ = succ


# In[102]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.succ({s0, s2}, 'b') == {s1}
assert auto1.succ({s0}, 'a') == {s0}
assert auto1.succ({s0, s1}, 'a') == {s0, s2}


# In[103]:


# Fournir un autre jeu de tests
# Fournir un autre jeu de tests 
assert auto1.succ({s0},'a') == {s0}
# voici un test faux de la fonction succ
assert (auto1.succ({s1},'a') == {s0})==False


# In[ ]:





# 2. Donner une définition de la fonction `accepte`
#   qui, étant donné une chaîne de caractères `mot`,
#   renvoie un booléen qui vaut vrai si et seulement si `mot` est accepté par l'automate. Attention, noter que l'automate peut ne pas être déterministe.

# In[104]:


# A faire 

def accepte(self, mot) :
    """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
    """
    final = self.getSetFinalStates()
    initial = self.getSetInitialStates()
    for c in mot:
        auto_succ = succ(self,initial,c)
        if(auto_succ==set()):
            return False
        initial=auto_succ
    for i in initial:
        return (i in final)

Automate.accepte = accepte


# In[105]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.accepte('aa') == False
assert auto1.accepte('ab') == False
assert auto1.accepte('aba') == True


# In[106]:


# Fournir un autre jeu de tests
# Fournir un autre jeu de tests
assert auto1.accepte('ababbaaba')
assert auto1.accepte('ababbaabaa')==False


# In[ ]:





# 3. Donner une définition de la fonction `estComplet`
#     qui, étant donné un automate `auto` et un ensemble de caractères `Alphabet`
#     renvoie un booléen qui vaut vrai si et
#     seulement si `auto` est complet par rapport à l'alphabet.
#     
#     On n'effectuera pas la vérification sur les états non accessibles depuis les états initiaux.

# In[107]:


# A faire 

def estComplet(self, Alphabet) :
    """ Automate x set[str] -> bool
        rend True si auto est complet pour les lettres de Alphabet, False sinon
        hyp : les éléments de Alphabet sont de longueur 1
    """
    states = self.allStates
    for a in Alphabet:
        for s in states:
            if(succElem(self,s,a)==set()):
                return False
    return True
       


Automate.estComplet = estComplet


# In[108]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.estComplet({'a', 'b'}) == True
assert auto1.estComplet({'a', 'c', 'b'}) == False


# In[109]:


# Fournir un autre jeu de tests
assert auto1.estComplet({'a'})==True


# In[ ]:





# 4. Donner une définition de la fonction `estDeterministe`
# qui, étant donné un automate `auto`,
#  renvoie un booléen qui vaut vrai si et seulement si `auto` est déterministe.

# In[110]:


# A faire 

def estDeterministe(self) :
    """ Automate -> bool
        rend True si auto est déterministe, False sinon
    """
    states = self.allStates
    transitions = self.allTransitions 
    if(len(self.getSetInitialStates())!=1):
        return False
    ens = set()
    for i in transitions:
        ens.add(i.etiquette)
    for s in states:
        for a in ens:
            if(len(succElem(self,s,a))>1):
                return False
    return True
    
Automate.estDeterministe = estDeterministe


# L'appel de fonction `copy.deepcopy(auto)` renvoie un nouvel automate identique à `auto`.

# In[111]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant, puis un jeu de tests :

auto1.show()
print('---')
assert auto1.estDeterministe() == True

auto1bis = copy.deepcopy(auto1)
#t : Transition
t = Transition(s1, 'b', s0)
auto1bis.addTransition(t)
auto1bis.show()
print('---')
assert auto1bis.estDeterministe() == False

auto1bis.removeTransition(t)
auto1bis.show()
print('---')
assert auto1bis.estDeterministe() == True


# In[112]:


# Fournir un autre jeu de tests
# Fournir un autre jeu de tests
t = Transition(s0, 'a', s2)
auto1bis.addTransition(t)
auto1bis.show()
print('---')
assert auto1bis.estDeterministe() == False


# In[ ]:





# 5. Donner une définition de la fonction `completeAutomate`
# qui, étant donné un automate `auto` et l'ensemble alphabet d'entrée `Alphabet`,
# renvoie l'automate complété d'`auto`.
#   
# Attention, il ne faut pas modifier `auto`, mais construire un nouvel automate.
# <br>Il pourra être intéressant d'utiliser l'appel de fonction
# `copy.deepcopy(auto)` qui renvoie un nouvel automate identique à `auto`.
# <br>On pourra faire appel à la fonction `nextId` afin de construire l'état $\bot$.

# In[113]:


# A faire
def completeAutomate(self, Alphabet) :
    """ Automate x str -> Automate
        rend l'automate complété de self, par rapport à Alphabet
    """        
    auto_c = copy.deepcopy(self)
    if auto_c.estComplet(Alphabet):return auto_c
    sn = State(auto_c.nextId(),False,False)
    auto_c.addState(sn)
    set_1 = auto_c.getSetInitialStates()
    while (auto_c.estComplet(Alphabet)==False):
        for l in Alphabet:
            for s in set_1:
                if len(auto_c.succElem(s,l))==0:
                    t = Transition(s,l,sn)
                    auto_c.addTransition(t)
        for l in Alphabet:
            set_1 = set_1.union(auto_c.succ(set_1,l))
    return auto_c

Automate.completeAutomate = completeAutomate


# In[114]:


# On a défini auparavant un automate auto1, voilà les résultats le concernant :

auto1.show()
print('---')
assert auto1.estComplet({'a', 'b'}) == True
auto1complet = auto1.completeAutomate({'a', 'b'})
auto1complet.show()
assert auto1complet.estComplet({'a', 'b'}) == True

print('---')
assert auto1.estComplet({'a', 'b', 'c'}) == False
auto1complet = auto1.completeAutomate({'a', 'b', 'c'})
auto1complet.show()
assert auto1complet.estComplet({'a', 'b','c'}) == True


# In[115]:



# Fournir un autre jeu de tests
auto2.show()
auto2.addTransition(Transition(s0,'c',s2))
auto2.addTransition(Transition(s2,'c',s1))
auto2.show()
auto2.completeAutomate({'a','b','c'})
auto2.show()


# In[ ]:





# ### 4. Déterminisation  <a class="anchor" id="sec4"></a>

# 1. Donner une définition de la fonction `newLabel`
# qui, étant donné un ensemble d'états renvoie une *chaîne de caractères* représentant l'ensemble de tous les labels des états.
# Par exemple, l'appel de `newLabel` sur un ensemble de 3 états dont les labels sont `'1', '2', '3'` renvoie `'{1,2,3}'`
# 
# Afin d'être assuré que l'ordre de parcours de l'ensemble des états n'a pas d'importance, il sera nécessaire de trier par ordre alphabétique la liste des `label` des états. On pourra faire appel à `L.sort()` qui étant donné la liste `L` de chaînes de caractères, la trie en ordre alphabétique.

# In[116]:




# A faire

def newLabel(S):
    """ set[State] -> str
    """
    liste = []
    for etat in S:
        liste.append(etat.label)
    liste.sort()
    res="{"
    for l in liste:
        if(l==liste[-1]):
            res+=l+"}"
        else:
            res+=l+","
    
    return res


# In[117]:


# On a défini auparavant un automate auto1, voilà un test le concernant :

assert newLabel(auto1.allStates) == '{0,1,2}'


# In[118]:


# Fournir un autre jeu de tests
assert (newLabel(auto1.allStates) == '{0,2}')== False


# La fonction suivante permet de déterminiser un automate. On remarque qu'un état peut servir de clé dans un dictionnaire.

# In[119]:


def determinisation(self) :
    """ Automate -> Automate
    rend l'automate déterminisé de self """
    # Ini : set[State]
    Ini = self.getSetInitialStates()
    # fin : bool
    fin = False
    # e : State
    for e in Ini:
        if e.fin:
            fin = True
    lab = newLabel(Ini)
    s = State(0, True, fin, lab)
    A = Automate(set())
    A.addState(s)
    Alphabet = {t.etiquette for t in self.allTransitions}
    Etats = dict()
    Etats[s] = Ini
    A.determinisation_etats(self, Alphabet, [s], 0, Etats, set())
    return A


# L'automate déterminisé est construit dans `A`. Pour cela la fonction récursive `determinisation_etats` modifie en place l'automate `A`, et prend en outre les paramètres suivants :
# - `auto`, qui est l'automate de départ à déterminiser
# - `Alphabet` qui contient l'ensemble des lettres étiquetant les transistions de l'automate de départ
# - `ListeEtatsATraiter` qui est la liste des états à ajouter et à traiter dans `A` au fur et à mesure que l'on progresse dans `auto`.
# - `i` qui est l'indice de l'état en cours de traitement (dans la liste `ListeEtatsATraiter`).
# - `Etats` qui est un dictionnaire dont les clés sont les états de `A` et les valeurs associées sont l'ensemble d'états issus de `auto` que cette clé représente.
# - `DejaVus` est l'ensemble des labels d'états de `A` déjà vus.

# In[120]:


# A faire 

def determinisation_etats(self, auto, Alphabet, ListeEtatsATraiter, i, Etats, DejaVus):
    """ Automate x Automate x set[str] x list[State] x int x dict[State : set[State]], set[str] -> NoneType
    """
    if (i>= len(ListeEtatsATraiter)):
        return;
    DejaVus.add(ListeEtatsATraiter[i].label)
    for lettre in Alphabet:
        ens=set()
        ens= auto.succ(Etats[ListeEtatsATraiter[i]],lettre)
        if ens!=set():
            fin=False
            for etat in ens:
                if etat.fin:
                    fin=True
                    break
            label = newLabel(ens)
            existe=False
            for s in self.allStates:
                if s.label==label:
                    etat=s
                    existe =True
                    break
            if (not existe):
                etat=State(self.nextId(),False,fin,label)
                self.addState(etat)
            Etats[etat]=ens
            self.addTransition(Transition(ListeEtatsATraiter[i],lettre,etat))
            if label not in DejaVus:
                ListeEtatsATraiter.append(etat)
        
        
    return determinisation_etats(self, auto, Alphabet, ListeEtatsATraiter, i+1, Etats, DejaVus)

Automate.determinisation_etats = determinisation_etats
Automate.determinisation = determinisation


# In[121]:


# Voici un test
#automate est l'automate construit plus haut a partir du fichier exempleAutomate.txt
automate = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
automate.show()
auto_det = automate.determinisation()
print(auto_det.estDeterministe())
auto_det.show(2)


# In[122]:


#Fournir d'autres jeux de tests
# Voici un test
#automate est l'automate construit plus haut a partir du fichier exempleAutomate.txt
automatebis = copy.deepcopy(auto2)
automatebis.addTransition(Transition(s0,'b',s2))
automatebis.show()
auto_detbis = automatebis.determinisation()
print(auto_detbis.estDeterministe())
auto_detbis.show(2)


# ### 5. Constructions sur les automates réalisant  des opérations sur les langages acceptés <a class="anchor" id="sec5"></a>
# 
# 
# #### 5.1 Opérations ensemblistes sur les langages <a class="anchor" id="sec5_1"></a>
# 
# 1. Donner une définition de la fonction `complementaire` qui, étant donné un automate `auto` et un ensemble de caractères `Alphabet`, renvoie l'automate acceptant la langage complémentaire du langage accepté par `auto`. Ne pas modifier l'automate `auto`, mais construire un nouvel automate.

# In[123]:


#A faire

def complementaire(self, Alphabet):
    """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de self
    """
    auto = completeAutomate(self,Alphabet)
    auto = determinisation(auto)
    etats = auto.allStates
    for etat in etats:
        if(etat.fin==True):
            etat.fin = False
        else:
            etat.fin = True
    return auto

    

Automate.complementaire = complementaire    


# In[124]:


# Voici un test

automate = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
automate.show()
Alphabet = {t.etiquette for t in auto.allTransitions}
auto_compl = automate.complementaire(Alphabet)
auto_compl.show(2)


# In[125]:


#Fournir d'autres tests

auto1.show()
auto1_compl=auto1.complementaire(['a','b'])
auto1_compl.show()


# 2. Donner une définition de la fonction `intersection` qui, étant donné deux automates `auto1` et `auto2`, renvoie l'automate acceptant l'intersection des langages acceptés par `auto1` et `auto2`.
# 
# L'automate construit ne doit pas avoir d'état non accessible depuis l'état initial.

# In[126]:


#A faire



def prodCartesien(E,F):
    """ set[type] x set[type] -> set[tuple[type]]
    """
    return {(e,f) for e in E for f in F}

def Prod(auto1,auto2):
    """ Automate x Automate -> Automate x dict[State : (State x State)]
        Calcul le produit cartesien de deux automates pour l'union et l'intersection
    """
    States=set()
    Transitions=set()
    dico={}
    Alphabet = {t.etiquette for t in auto1.allTransitions} | {t.etiquette for t in auto2.allTransitions}
    for s1 in auto1.allStates:
        for s2 in auto2.allStates:
            if(not(s1,s2) in dico.keys()):
                s=State(len(States), s1.init and s2.init,False,"("+str(s1.label)+","+str(s2.label)+")")
                States.add(s)
                dico[(s1,s2)]=s
            else:
                s=dico[(s1,s2)]
            for a in Alphabet:
                # print(prodCartesien(auto1.succElem(s1,a),auto2.succElem(s2,a)))
                for t in prodCartesien(auto1.succElem(s1,a),auto2.succElem(s2,a)):
                    if(not(t in dico.keys())):
                        s_prime=State(len(States),t[0].init and t[1].init,False,"("+str(t[0].label)+","+str(t[1].label)+")")
                        dico[t]=s_prime
                        States.add(s_prime)
                    else:
                        s_prime=dico[t]
                    Transitions.add(Transition(s,a,s_prime))
                    # Automate(Transitions).show()
    
    return Automate(Transitions),dico


def intersection(self, auto):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage l'intersection des langages des deux automates
    """
    auto_r,dico=Prod(self,auto)
    for couple in prodCartesien(self.allStates,auto.allStates):
        dico[couple].fin=couple[0].fin and couple[1].fin
    return auto_r
    
Automate.intersection = intersection


# In[127]:


#Un premier test

automate.show()
auto2.show()
inter = automate.intersection(auto2)
inter.show(2)


# In[128]:


# Fournir d'autres tests
automatebis.show()
auto2.show()
interbis = automatebis.intersection(auto2)
interbis.show(2)


# 3. (Question facultative) Donner une définition de la fonction `union` qui, étant donné deux automates `auto1` `auto2`, renvoie l'automate acceptant comme langage l'union des langages acceptés par `auto1` et `auto2`.

# In[129]:


#A faire par l'étudiant


def union (self, auto):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage l'union des langages des deux automates
    """
    auto_res,dico=Prod(self,auto)
    for couple in prodCartesien(self.allStates,auto.allStates):
        dico[couple].fin=couple[0].fin or couple[1].fin
    return auto_res

Automate.union = union  


# In[130]:


#Un premier test

automate.show()
auto2.show()
uni = automate.union(auto2)
uni.show(2)

#test

automatebis.show()
auto2.show()
unibis = automatebis.union(auto2)
unibis.show(1)


# #### 5.2 Opérations rationnelles sur les langages <a class="anchor" id="sec5_2"></a>
# 
# Programmer *une des deux* méthodes suivantes:
# 
# 1. Donner une définition de la fonction `concatenation` qui, étant donné deux automates `auto1` et `auto2`, renvoie l'automate acceptant comme langage la concaténation des langages acceptés par `auto1` et `auto2`.
# 
# 2. Donner une définition de la fonction `etoile` qui, étant donné un automate `auto`, renvoie l'automate acceptant comme langage l'étoile du langages accepté par `auto`.

# In[131]:


def concatenation (self, auto):
    """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
    transitions = set()

    for etat1 in auto1.allStates:
        if etat1.fin:
            etat_fin=State(etat1.id,False,False)         
    for etat2 in auto2.allStates:
        if etat2.init:
            etat_initial=State(etat2.id,False,False)   
    for transition in auto1.allTransitions:
        if (((transition.stateDest).fin) and (not ((transition.stateSrc).fin))):
            tc=Transition(transition.stateSrc,transition.etiquette,etat_initial)
            transitions.add(tc)
        if (((transition.stateDest).fin) and ((transition.stateSrc).fin)):
            tc=Transition(etat_fin,transition.etiquette,etat_initial)
            transitions.add(tc)
        if (((transition.stateDest).fin) and (not ((transition.stateSrc).fin))):
            tn=Transition(transition.stateSrc,transition.etiquette,etat_fin)
            transitions.add(tn)
        elif (((not ((transition.stateDest).fin))) and ((transition.stateSrc).fin)):
            tn=Transition(etat_fin,transition.etiquette,transition.stateDest)
            transitions.add(tn)
        elif (((transition.stateDest).fin) and ((transition.stateSrc).fin)):
            tn=Transition(etat_fin,transition.etiquette,etat_fin)
            transitions.add(tn)
        else:
            transitions.add(transition)
    for transition in auto2.allTransitions:
        if (not (transition.stateDest).init) and (transition.stateSrc).init:
            tn=Transition(etat_initial,transition.etiquette,transition.stateDest)
            transitions.add(tn)
        elif (transition.stateDest).init and not (transition.stateSrc).init:
            tn=Transition(transition.stateSrc,transition.etiquette,etat_initial)
            transitions.add(tn)
        elif (transition.stateDest).init and (transition.stateSrc).init:
            tn=Transition(etat_initial,transition.etiquette,etat_initial)
            transitions.add(tn)
        else:
            transitions.add(transition)
    liste_res=[]
    for t in transitions:
        liste_res.append(t)
    auto=Automate(liste_res)
    return auto

Automate.concatenation = concatenation


# In[132]:


#Un premier test

automate.show()
auto2.show()
concat = automate.concatenation(auto2)
concat.show(2)


# In[133]:


#Fournir un autre jeu de test
#Fournir un autre jeu de test
automatebis.show()
auto2.show()
concatbis = automatebis.concatenation(auto2)
concatbis.show(2)


# In[134]:


def etoile (self):
    """ Automate  -> Automate
    rend l'automate acceptant pour langage l'étoile du langage de a
    """
    copie = copy.deepcopy(self)
    alphabet = {a.etiquette for a in copie.allTransitions}
    
    for etat in copie.allStates:
        for lettre in alphabet:
            etatsSucc = copie.succElem(etat, lettre)
            for e in etatsSucc:
                if e.fin:
                    for i in copie.getSetInitialStates():
                        copie.addTransition(Transition(etat, lettre, i))
    
    for etat in copie.allStates:
        if etat.init:
            etat.fin = True
            break
    return copie
            
Automate.etoile = etoile


# In[135]:


#Un premier test

automate.show()
autoetoile = automate.etoile()
autoetoile.show()


# In[136]:


#Fournir un autre jeu de tests
automatebis.show()
autoetoilebis = automatebis.etoile()
autoetoilebis.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





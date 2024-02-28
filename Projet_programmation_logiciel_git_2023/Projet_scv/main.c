#include "header.h"
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h> 
#include <sys/types.h>


int main() {

  // Exemple d'utilisation des fonctions de la liste chaînée

  // Initialiser une liste
  List *L = initList();

  // Insérer des éléments dans la liste
  Cell *C1 = buildCell("Element 1");
  Cell *C2 = buildCell("Element 2");
  Cell *C3 = buildCell("Element 3");
  insertFirst(L, C1);
  insertFirst(L, C2);
  insertFirst(L, C3);

  // Afficher le contenu de la liste
  char* lto=ltos(L);
  printf("Contenu de la liste : %s\n", lto);
  free(lto);
  // Obtenir un élément à partir de l'index
  int index = 1;
  Cell *result = listGet(L, index);
  if (result != NULL) {
    printf("Element à l'index %d : %s\n", index, ctos(result));

  } else {
    printf("Index invalide : %d\n", index);
  }

  // Convertir la liste en chaîne de caractères
  char *listeStr = ltos(L);
  printf("Liste convertie en chaîne de caractères : %s\n", listeStr);

  // Rechercher un élément dans la liste
  char *str = "Element 2";
  Cell *result2 = searchList(L, str);
  if (result2 != NULL) {
    printf("Element trouvé : %s\n", ctos(result2));
  } else {
    printf("Element non trouvé : %s\n", str);
  }

  // Libérer la mémoire allouée pour la liste
  liberer(L);
  free(listeStr);
  
 
/////////////////////////////////////////////
  
    WorkTree* wt = initWorkTree();
   
  int i= appendWorkTree(wt, "siwar1", "1", 0);
   i= appendWorkTree(wt, "siwar2", "2", 0);
   i= appendWorkTree(wt, "siwar3", "3", 0);
   printf("%d\n",i);
  printf("%d\n",inWorkTree( wt, "siwar2"));
  char* ch=wtts( wt);
  printf("%s\n",ch);
  free(ch);
  WorkTree* wt2 = initWorkTree();
    appendWorkTree(wt2, "file1.txt", "abcd1234", 644);
    appendWorkTree(wt2, "file2.txt", "efgh5678", 777);
    char* hash = blobWorkTree(wt2);
    printf("Hash du fichier temporaire : %s\n", hash);
    free(hash);
     freeWorkTree(wt2);
     freeWorkTree(wt);
//////////////////////////////////////////////////
// Création d'un commit
  Commit *commit = createCommit("abcdefg12345");

  // Ajout d'éléments dans le commit
  commitSet(commit, "author", "John Doe");
  commitSet(commit, "date", "2023-04-17");
  commitSet(commit, "message", "Example commit");

  // Affichage du commit
  char *commitStr = cts(commit);
  printf("Commit:\n%s\n", commitStr);
  free(commitStr);

  // Récupération de la valeur d'un élément dans le commit
  char *author = commitGet(commit, "author");
  printf("Author: %s\n", author);

  // Libération de la mémoire allouée
  freeCommit(commit);
	
    return 0;
}


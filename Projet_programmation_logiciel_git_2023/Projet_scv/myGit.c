#include "header.h"

int main(int argc, char *argv[]) {

  /*argv[0] contient toujours la commande d'exécution ./myGit */
  if (strcmp(argv[1], "init") == 0) {
    initRefs();
    initBranch(); // initialisation des repertoires
  }

  if (strcmp(argv[1], "list-refs") == 0) {
    printf("REFS : \n");
    if (file_exists(".refs")) {
      List *list_refs = listdir(".refs");
      Cell *tmp = *list_refs;
      while (tmp) {
        if (tmp->data[0] !=
            '.') { // si ce n'est pas le repertoire lui meme on ajoute les fichiers ou les sous repertoires
          printf("- %s : %s\n", tmp->data, getRef(tmp->data));
        }
        tmp = tmp->next;
      }
      liberer(list_refs);
    } else {
      printf("pas de reference\n");
    }
  }

  if (strcmp(argv[1], "create-ref") == 0) {
    createUpdateRef(argv[2], argv[3]); // création de la référence
  }

  if (strcmp(argv[1], "delete-ref") == 0) {
    deleteRef(argv[2]); // suppression de la référence
  }

  if (strcmp(argv[1], "add") == 0) {
    for (int i = 2; i < argc; i++) {
      myGitAdd(argv[i]); // ajout à la zone de préparation
    }
  }
  if (strcmp(argv[1], "list-add") == 0) {
    printf("Zone de préparation : \n");
    if (file_exists(".add")) {
      system("cat .add"); // affichage du contenu de la zone de préparation
    }
  }

  if (strcmp(argv[1], "clear-add") == 0) {
    system("rm .add"); // on vide la zone de préparation
    printf("add vidé\n");
  }
  if (strcmp(argv[1], "commit") == 0) {
    if (argc > 3 && strcmp(argv[3], "-m") == 0) {
      char message[256] = "";
      for (int i = 4; i < argc - 1; i++) {
        strcat(message, argv[i]); // il peut y avoir des espaces donc recupere
                                  // toute la chaine
        strcat(message, " ");
      }
      strcat(message, argv[argc - 1]);
      myGitCommit(argv[2], message); //
    } else {                         // s'il n'y a pas de message
      myGitCommit(argv[2], NULL);
    }
  }
  if (strcmp(argv[1], "get-current-branch") == 0) {
    char *current_branch = getCurrentBranch();
    printf("branche courant : %s\n", current_branch);
    free(current_branch);
  }
  if (strcmp(argv[1], "branch") == 0) {
    if (branchExists(argv[2]) == 0) { // si la branche n'existe pas déjà
      createBranch(argv[2]);
    } else { // si la branche existe déjà
      printf("La branche existe !\n");
    }
  }
  if (strcmp(argv[1], "branch-print") == 0) {
    if (!branchExists(argv[2])) { // si la branche n'existe pas
      printf("ERREUR : la branche n'existe pas !\n");
    } else { // si elle existe
      printBranch(argv[2]);
    }
  }
  if (strcmp(argv[1], "checkout-branch") == 0) {
    if (!branchExists(argv[2])) {
      printf("ERREUR : la branche n'existe pas !\n");
    } else {
      myGitCheckoutBranch(argv[2]);
    }
  }
  if (strcmp(argv[1], "checkout-commit") == 0) {

    myGitCheckoutCommit(argv[2]);
  }

    
  if (strcmp(argv[1], "merge") == 0) {

    char *current_branch = getCurrentBranch();
    List *conflicts = merge(argv[2], argv[3]);

    if (*conflicts == NULL) {
      printf("La fusion s'est bien passée\n");
    } else {
      printf("La fusion ne s'est pas passée comme prévu, choisir une option "
             "parmi les suivantes: \n ");
      printf("Tapez 1 pour Garder les fichiers de la branche courante\n");
      printf("Tapez 2 pour Garder les fichiers de la branche %s\n", argv[2]);
      printf("Tapez 3 pour choisir manuellement, conflit par conflit\n");
      printf("Choix entre 1 et 3 : \n");
      int choix;
      scanf("%d", &choix);
      if (choix == 1) {
        createDeletionCommit(argv[2], conflicts, argv[3]);
        merge(argv[2], argv[3]);
      }
      if (choix == 2) {
        createDeletionCommit(getCurrentBranch(), conflicts, argv[3]);
        merge(argv[2], argv[3]);
      }
      if (choix == 3) {
        List *conflicts_current = initList();
        List *conflicts_remote = initList();
        Cell *fichier = *conflicts;
        printf("Branche courante :  %s\nBranche remote : %s\n",getCurrentBranch(), argv[2]);
        int choix;
        while (fichier != NULL) {
          printf(
              "choisissez la branche dans laquelle vous voulez garder le fichier %s\nPour celà, Tapez 1 pour la garder dans la branche courante et tapez 2 pour le mettre dans la branche remote\n",
              fichier->data);
          scanf("%d", &choix);
          if (choix == 1) {
            insertFirst(conflicts_current, buildCell(fichier->data));
          }
          else if(choix == 2) {
            insertFirst(conflicts_remote, buildCell(fichier->data));
          } else {
            printf("ERREUR, le fichier est placé dans la branche courante\n");
            insertFirst(conflicts_current, buildCell(fichier->data));
          }
          fichier = fichier->next;
        }
        createDeletionCommit(getCurrentBranch(), conflicts_current, argv[3]);
        createDeletionCommit(argv[2], conflicts_remote, argv[3]);
        merge(argv[2], argv[3]);
        printf("La fusion s'est bien passée\n");
          //liberer(conflicts_current);
           //liberer(conflicts_remote);
           //liberer(&fichier);
      } else {
        printf("choix impossible, recommencez !\n");
      }
    }
      free(current_branch);
      //liberer(conflicts);
  }
  //////////////////////////////////////////////////////////////

  return 0;
}

#include "header.h"

// initialisation du fichier branche courante

void initBranch() {
  FILE *f = fopen(".current_branch", "w");
  fprintf(f, "master");
  fclose(f);
}

// teste si la branche existe

int branchExists(char *branch) {
  List *l = listdir(".refs");
  if (searchList(l, branch) != NULL) {
    liberer(l);
    return 1;
  } else {
    liberer(l);
    return 0;
  }
}

// cree une branche

void createBranch(char *branch) {
  if (branchExists(branch) == 1) {
    printf("la branche existe déjà\n");
    return;
  }
  char HEAD[15] = ".refs/HEAD";
  char chaine[70];
  sprintf(chaine, "cat %s > .refs/%s", HEAD,
          branch); // copie le hash du HEAD dans branch
  system(chaine);
}

// montre la branche courante

char *getCurrentBranch() {
  FILE *f = fopen(".current_branch", "r");
  char *buffer = malloc(256 * sizeof(char));
  fgets(buffer, 256, f);
  fclose(f);
  return buffer;
}

// affiche le contenu de la branche

void printBranch(char *branch) {
  char *hashCommit = getRef(branch); // recupere le hash de branch
  if (hashCommit == NULL || strlen(hashCommit) == 0) {
    return;
  }
  hashCommit[strlen(hashCommit) - 1] = '\0';
  char *hashPathCommit = malloc(SIZEMAX_CHAR * sizeof(char));
  char *path = malloc((SIZEMAX_CHAR + 3) * sizeof(char));
  strcpy(path, hashToPath(hashCommit));
  sprintf(hashPathCommit, "%s.c",
          path);                   // cree le format hash du chemin du commit
  Commit *c = ftc(hashPathCommit); // cree le commit
  while (c != NULL) {
    if (commitGet(c, "message") != NULL) {
      printf("%s : %s\n", hashCommit, commitGet(c, "message"));
    } else {
      // y'a pas de message
      printf("%s\n", hashCommit);
    }
    if (commitGet(c, "predecessor") != NULL) {
      hashCommit = commitGet(c, "predecessor");
      strcpy(path, hashToPath(hashCommit));
      sprintf(hashPathCommit, "%s.c", path);
      c = ftc(hashPathCommit); // c devient le commit d'avant s'il existe
    } else {
      c = NULL;
    }
  }
    free(hashPathCommit);
    free(path);
    free(hashCommit);
}
	


// retourne la liste des commits de la branch
List *branchList(char *branch) {
  List *L = initList();
  char *commit_hash = getRef(branch);
  if (commit_hash == NULL) {
    liberer(L);
    free(commit_hash);
    return NULL;
  } else if (strlen(commit_hash) == 0) {
    return L;
  }
  // on recupere le hash du chemin
  char *commit_path = hashToPathCommit(commit_hash);
  printf("le hash du commit : %s\n", commit_path);
  Commit *c = ftc(commit_path);
  // on parcourt tous les commits
  while (c) {
    insertFirst(L, buildCell(commit_hash));
    if (commitGet(c, "predecessor") == NULL) { // la fonction s'arrete
      break;
    } else { // on continue
      char *ref = commit_hash;
      commit_hash = commitGet(c, "predecessor");
      free(ref); // on libere sequentiellement la memoire
      char *path = commit_path;
      commit_path = hashToPathCommit(commit_hash);
      free(path);
      c = ftc(commit_path); // pour cree le commit du predecesseur
    }
  }
  free(commit_hash);
  free(commit_path);
  // freeCommit(c);
  return L;
}

// recupere tous les commits
List *getAllCommits() {
  List *L = initList();
  List *list = listdir(".refs");
  Cell *cl = *list;
  while (cl) {
    if (cl->data[0] != '.') { // si cl est une branche
      List *list2 = branchList(cl->data);
      Cell *cell = *list2;
      while (cell) {
        if (!searchList(L, cell->data)) {
          Cell *cellule = buildCell(cell->data);
          // si le commit n'est pas dans la liste on la selectionne
          insertFirst(L, cellule);
        }
        cell = cell->next;
      }
      liberer(list2);
    }
    cl = cl->next;
  }
  liberer(list);
  return L;
}

// restauration du commit

void restoreCommit(char *hash_commit) {
  // meme processus que l'autre restore
  char *hashPathCommit = hashToPathCommit(hash_commit);
  Commit *c = ftc(hashPathCommit);
  char *tree_hash = hashToPath(commitGet(c, "tree"));
  tree_hash[65] = '.';
  tree_hash[66] = 't';
  tree_hash[67] = '\0';
    //on procede de cette maniere car implicitement ça nous met un \n au 65eme caractere et on ne sait pas pourquoi
  WorkTree *wt = ftwts(tree_hash);
  restoreWorkTree(wt, ".");
  free(hashPathCommit);
  free(tree_hash);
}

// permet de se deplacer sur la nouvelle branche

void myGitCheckoutBranch(char *branch) {
  FILE *f = fopen(".current_branch", "w");
  fprintf(f, "%s", branch);
  fclose(f); // on met a jour la branche comme etant une branche courante
  char *ref = getRef(branch);
  FILE *b = fopen(".refs/HEAD", "w");
  fprintf(b, "%s", ref);
  fclose(b); // on fait pointer HEAD sur la branche
  char *refB = getRef(branch);
  // si aucun commit dans la 2e branche, on a rien a recuperer
  if (refB != NULL && strlen(refB) != 0) {
    restoreCommit(refB); // on restaure
  }
  free(ref);
  free(refB);
}

// filtre une liste à partir de son pattern

List *filterList(List *L, char *pattern) {
  List *filtre = initList();
  int n = strlen(pattern);
  Cell *c = *L;
  // printf("pattern : %s\n", pattern);
  while (c) {
    // printf("c(data) : %s", c->data);
    if (strncmp(c->data, pattern, n) ==
        0) { // compare les deux chaines de longueur pattern
      // printf("c(data) : %s, pattern : %s\n", c->data, pattern);
      insertFirst(filtre, buildCell(c->data));
    }
    c = c->next;
  }
  return filtre;
}

// permet de retourner sur une ancienne version de nos fichiers

void myGitCheckoutCommit(char *pattern) {
  List *allC = getAllCommits();
  List *allCPattern = filterList(allC, pattern); // on filtre d'abord
  Cell *c = *allCPattern;
  if (c == NULL) {
    printf("PAS DE HASH - ERREUR ! \n");
    return;
  }
  if ((c->next == NULL) || (c->next->data == NULL)) {
    // on checkout la branche du commit
    char *commitHash = (listGet(allCPattern, 0))->data;
    FILE *b = fopen(".refs/HEAD", "w");
    fprintf(b, "%s", commitHash); // on fait pointer head dans le commit
    fclose(b);
    restoreCommit(commitHash); // on restaure
      free(commitHash);
    return;
  }
  printf("liste pattern : %s\n", ltos(allCPattern));
  printf("Precisez votre requete ! \n");
  liberer(allCPattern);
  liberer(allC);
  return;
}

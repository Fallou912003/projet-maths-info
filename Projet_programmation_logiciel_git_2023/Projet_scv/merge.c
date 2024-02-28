#include "header.h"
// fait le merge de deux worktree

WorkTree *mergeWorkTrees(WorkTree *wt1, WorkTree *wt2, List **conflicts) {

    List * conflicts1 = initList();
    WorkTree *fusion = initWorkTree();
    
    int k;
    for (int i = 0; i < wt1->n; i++) {

        k = inWorkTree(wt2, wt1->tab[i].name);

        if(k<0){
            if(inWorkTree(fusion, wt1->tab[i].name)==-1){
                appendWorkTree(fusion, wt1->tab[i].name, wt1->tab[i].hash, wt1->tab[i].mode);
            }
        }

        else if(strcmp(wt1->tab[i].hash, wt2->tab[k].hash) == 0){
            if(inWorkTree(fusion, wt1->tab[i].name)==-1){
                appendWorkTree(fusion, wt1->tab[i].name, wt1->tab[i].hash, wt1->tab[i].mode);
            }
        }

        else{
            if(searchList(conflicts1, wt1->tab[i].name)==NULL){
                insertFirst(conflicts1, buildCell(wt1->tab[i].name));
            }
        }

    }

    // Deuxieme WorkTree : pareil

    for (int i = 0; i < wt2->n; i++) {

        k = inWorkTree(wt1, wt2->tab[i].name);

        if(k<0){
            if(inWorkTree(fusion, wt2->tab[i].name)==-1){
                appendWorkTree(fusion, wt2->tab[i].name, wt2->tab[i].hash, wt2->tab[i].mode);
            }
        }

        else if(strcmp(wt2->tab[i].hash, wt1->tab[k].hash) == 0){
            if(inWorkTree(fusion, wt2->tab[i].name)==-1){
                appendWorkTree(fusion, wt2->tab[i].name, wt2->tab[i].hash, wt2->tab[i].mode);
            }
        }

        else{
            if(searchList(conflicts1, wt2->tab[i].name)==NULL){
                insertFirst(conflicts1, buildCell(wt2->tab[i].name));
            }
        }

    }
  
    *conflicts = conflicts1;
    return fusion;
}
// merge deux branches sans conflits

List *merge(char *remote_branch, char *message) {

  char *current_branch = getCurrentBranch(); // on recupere les branches
  char *Cremote = getRef(remote_branch);
  char *Ccurrent = getRef(current_branch);
  // Branch Remote
  char *hashPathCommitR = malloc(300 * sizeof(char));
  char *path = malloc(100 * sizeof(char));
  strcpy(path, hashToPath(Cremote));
  path[strlen(path) - 1] = '\0';
  sprintf(hashPathCommitR, "%s.c", path);
  Commit *cR = ftc(hashPathCommitR); // commit du remote
  char *tree_hashR = malloc(300 * sizeof(char));
  strcpy(tree_hashR, hashToPath(commitGet(cR, "tree")));
  strcat(tree_hashR, ".t");
  WorkTree *wtR = ftwts(tree_hashR); // wt du remote
  // Current Branch
  char *hashPathCommitC = malloc(300 * sizeof(char));
  char *pathC = malloc(100 * sizeof(char));
  strcpy(pathC, hashToPath(Ccurrent));
  pathC[strlen(pathC) - 1] = '\0';
  sprintf(hashPathCommitC, "%s.c", pathC);
  sprintf(hashPathCommitC, "%s.c", pathC);
  Commit *cC = ftc(hashPathCommitC); // commit current branch
  char *tree_hashC = malloc(300 * sizeof(char));
  strcpy(tree_hashC, hashToPath(commitGet(cC, "tree")));
  strcat(tree_hashC, ".t");
  WorkTree *wtC = ftwts(tree_hashC); // wt current branch
  List *conflicts = initList();
  WorkTree *fusion = mergeWorkTrees(wtR, wtC, &conflicts);
  // recuperation des fichiers fusion et mise à jour de conflits en fusionnant
  // les deux worktree
  if (*conflicts == NULL) {
    char *hashNewCommit = saveWorkTree(fusion, "."); // sauvegarde du worktree
    Commit *newC = createCommit(hashNewCommit);
    commitSet(newC, "predecessor", Ccurrent);
    commitSet(newC, "merged_predecessor", Cremote);
    commitSet(newC, "message", message); // 2 predecesseurs
    char *hashNewC = blobCommit(newC);   // enregistrement du commit
    FILE *b = fopen(".refs/HEAD", "w");
    fprintf(b, "%s\n",
            hashNewC); // HEAD va pointer sur le commit de la nouvelle branche
    fclose(b);
    char path[256];
    sprintf(path, ".refs/%s", current_branch);
    FILE *br = fopen(path, "w"); // la branche courante change
    fprintf(br, "%s\n", hashNewC);
    fclose(br);
    deleteRef(remote_branch);     // on supprime la reference remote
    restoreWorkTree(fusion, "."); // restauration du worktree de fusion
      free(hashNewCommit);
      free(hashNewC);
  }
    free(current_branch);
    free(Cremote);
    free(Ccurrent);
    free(hashPathCommitR);
    free(path);
    freeCommit(cR);
    free(tree_hashR);
    freeWorkTree(wtR);
    free(hashPathCommitC);
    free(pathC);
    freeCommit(cC);
    free(tree_hashC);
    freeWorkTree(wtC);
  return conflicts; // on retourne conflits qui peut etre nulle s'il rentre 
}

//creation de la commit de supression

void createDeletionCommit(char *branch, List *conflicts, char *message) {
  char *current_branch = getCurrentBranch(); // recuperation branche courante
  myGitCheckoutBranch(branch); // on se deplace sur la branche en parametre
  char *hBranch = getRef(branch);
  char *hPathC = malloc(300 * sizeof(char));
  char *pathC = malloc(100 * sizeof(char));
  strcpy(pathC, hashToPath(hBranch));
  pathC[strlen(pathC) - 1] = '\0';
  sprintf(hPathC, "%s.c", pathC);
  sprintf(hPathC, "%s.c", pathC);
  Commit *c = ftc(hPathC); // recupere le commit de la branche
  char *ht = malloc(300 * sizeof(char));
  strcpy(ht, hashToPath(commitGet(c, "tree")));
  strcat(ht, ".t");
  WorkTree *wt = ftwts(ht); // recupere le worktree de la branche
  deleteRef(".add");        // on supprime la zone de preparation
  for (int i = 0; i < wt->n; i++) {
    char *nom_fichier = (wt->tab[i]).name;
    if (searchList(conflicts, nom_fichier) != NULL) {
      // si le fichier de la branche est un fichier de conflit on l'ajoute dans
      // la zone de suppression
      myGitAdd(nom_fichier);
    }
  }
  myGitCommit(branch, message);        // on sauvegarde le commit branch
  myGitCheckoutBranch(current_branch); // on retourne sur la branche de base
    free(current_branch);
    free(hBranch);
    free(hPathC);
    free(pathC);
    //freeCommit(c);
    free(ht);
    //freeWorkTree(wt);
}

#include "header.h"
#define TAILLE 3


// 4.1 cree un workfile
WorkFile *createWorkFile(char *name) {
  WorkFile *wf = (WorkFile *)malloc(sizeof(WorkFile));
  wf->name = strdup(name);
  wf->hash = NULL;
  wf->mode = 0;
  return wf;
}

// 4.2 tranforme un workfile en chaine de caractere
char *wfts(WorkFile *wf) {
  if (wf == NULL) {
    return "";
  }
  char temp[1000];
  sprintf(temp, "%s\t%s\t%o%c", wf->name, wf->hash, wf->mode, '\0');
  char *res = strdup(temp);
  return res;
}

// 4.3 transforme une chaine de caractere representant un workfile en un
// workfile
WorkFile *stwf(char *ch) {
  char buff[100];
  char buff2[100];
  int buff3;
  sscanf(ch, "%s\t%s\t%o", buff, buff2, &buff3);
  WorkFile *res = createWorkFile(buff);
  res->hash = strdup(buff2);
  res->mode = buff3;
  return res;
}

// 4.4 initialise un worktree
WorkTree *initWorkTree() {
  WorkTree *wt = (WorkTree *)malloc(sizeof(WorkTree));
  wt->size = TAILLE;
  wt->n = 0;
  wt->tab = (WorkFile *)malloc(TAILLE * sizeof(WorkFile));
  return wt;
}

// 4.5 regarde si le workfile de nom name est dans le worktree
int inWorkTree(WorkTree *wt, char *name) {
  WorkFile *tmp = wt->tab;
  int pos = 0;
  while (pos < wt->n) {
    if (strcmp(tmp[pos].name, name) == 0)
      return pos;
    pos++;
  }
  return -1;
}

// 4.6 ajoute le workfile daans le worktree
int appendWorkTree(WorkTree *wt, char *name, char *hash, int mode) {
  if (inWorkTree(wt, name) != -1) // le workfile de ce nom est deja dedans
    return 0;
  if (wt->n >= wt->size) // le worktree est rempli
    return -1;

  (wt->tab)[wt->n].name = name ? strdup(name) : NULL;
  (wt->tab)[wt->n].hash = hash ? strdup(hash) : NULL;
  (wt->tab)[wt->n].mode = mode;
  (wt->n)++;

  return 1;
}

// (facultative) ajoute le workfile daans le worktree
int appendWorkTreeWf(WorkTree *wt, WorkFile *wf) {
  return appendWorkTree(wt, wf->name, wf->hash, wf->mode);
}

// 4.7 renvoie la chaine qui represente un worktree en utilisant la fonction
// wfts
char *wtts(WorkTree *wt) {
  if (wt->n == 0)
    return "";
  char *s = (char *)malloc(sizeof(char) * TAILLE * 1000);
  char *temp = wfts(&(wt->tab[0]));
  strcpy(s, temp);
  for (int i = 1; i < wt->n; i++) {
    char *temp2 = wfts(&(wt->tab[i]));
    strcat(s, "\n");
    strcat(s, temp2);
    free(temp2);
  }
  strcat(s, "\n");
  free(temp);
  return s;
}

// 4.8 renvoie le worktree qui represente la chaine ch
WorkTree *stwt(char *ch) {

  WorkTree *wt = initWorkTree();
  char *tmp = strdup(ch);
  char *token = strtok(tmp, "\n");
  int i = 0;
  while (token && i < wt->size) {
    WorkFile *wf = stwf(token);
    appendWorkTreeWf(wt, wf);
    token = strtok(NULL, "\n");
    freeWorkFile(wf);
    i++;
  }
  free(tmp);
  return wt;
}

// 4.9 ecrit le worktree dans le fichier file
int wttf(WorkTree *wt, char *file) {
  FILE *f = fopen(file, "w");
  char *temp = wtts(wt);
  fprintf(f, "%s", temp);
  fclose(f);
  free(temp);
  return 0;
}

// 4.10 renvoie le worktree du fichier file
WorkTree *ftwts(char *file) {
  FILE *fr;
  if ((fr = fopen(file, "r")) == NULL)
    return NULL;
  WorkTree *wt = initWorkTree();
  char buf[256];
  while (fgets(buf, 256, fr) != NULL) {
    WorkFile *wf = stwf(buf);
    if (wf != NULL) {
      appendWorkTree(wt, wf->name, wf->hash, wf->mode);
      freeWorkFile(wf);
    }
  }
  fclose(fr);
  return wt;
}

//(facultative) affiche le worktree
void printWorkTree(WorkTree *wt) {
  printf("WorkTree - Size: %d\n", wt->size);
  printf("------------------------------\n");
  for (int i = 0; i < wt->size; i++) {
    printf("File %d:\n", i + 1);
    printf("  Name: %s\n", wt->tab[i].name);
    printf("  Hash: %s\n", wt->tab[i].hash);
    printf("  Mode: %d\n", wt->tab[i].mode);
    printf("--------------------------\n");
  }
}

// 5.1 retourne le hash du chemin du fichier
char *hashToFile(char *hash) {
  char *ch2 = strdup(hash);
  ch2[2] = '\0';
  struct stat st;
  if (stat(ch2, &st) == -1) {
    mkdir(ch2, 0700);
  }
  free(ch2);
  return hashToPath(hash);
}

// retourne le hash du fichier temporaire et fait l'enregistrement instantané du
// worktree
char *blobWorkTree(WorkTree *wt) {
  char fname[100] = "/tmp/myfileXXXXXX";
  mkstemp(fname);
  wttf(wt, fname);                // ecrit le worktree dans le fichier temp
  char *hash = sha256file(fname); // hash du fichier temp
  char *ch = hashToFile(hash);
  strcat(ch, ".t");
  cp(ch, fname); // le contenu du fichier temp à l'enregistrement
  setMode(0777, ch);
  char *supp = malloc(100 * sizeof(char));
  sprintf(supp, "rm %s", fname);
  system(supp); // suppression du fichier temporaire fname
  free(ch);
  free(supp);
  return hash;
}

// libere le workfile
void freeWorkFile(WorkFile *wf) {
  if (wf) {
    free(wf->name);
    free(wf->hash);
    free(wf);
  }
  return;
}

// libere le worktree (on prefere reprendre le code du workfile caar ça nous
// fait des problemes si on utilise freeWorkFile car le worktree n'a pas de
// double pointeur
void freeWorkTree(WorkTree *wt) {
  int i = 0;
  WorkFile *p = wt->tab;
  while (i < wt->n) {
    WorkFile *wf = &(wt->tab[i]);
    // freeWorkFile(wf);
    free(wf->name);
    free(wf->hash);
    // free(wf);
    i++;
  }
  free(p);
  free(wt);
}

// regarde si path est un repertoire
int isDirectory(const char *path) {
  struct stat path_stat;
  stat(path, &path_stat);
  return S_ISDIR(path_stat.st_mode);
}

// concatenation avec /
char *concat_paths(char *path1, char *path2) {
  char *result = malloc(strlen(path1) + strlen(path2) + 2);
  strcpy(result, path1); // Copy path1 to result
  strcat(result, "/");   // Append a slash to result
  strcat(result, path2); // Append path2 to result
  return result;
}

// sauvegarde du worktree et de tout son contenu
char *saveWorkTree(WorkTree *wt, char *path) {
  for (int i = 0; i < wt->n; i++) {
    WorkFile *wf = &(wt->tab[i]);
    char *absPath = concat_paths(path, wf->name);
    if (isDirectory(absPath) == 0) { // fichier
      blobFile(absPath);             // on enregistre le fichier workfile
      wt->tab[i].hash = sha256file(absPath);
      wt->tab[i].mode = getChmod(absPath);
      //printf("Dans save, mode de wt->tab[i] = %o\n", wt->tab[i].mode);

    } else { // repertoire
      WorkTree *wt2 = initWorkTree();
      List *L = listdir(absPath); // on recupere la liste des fichiers ou
                                  // sous-repertoires dans le repertoire
      for (Cell *ptr = *L; ptr != NULL; ptr = ptr->next) {
        if (ptr->data[0] == '.')
          continue; // on ignore le repertoire lui mleme
        appendWorkTree(wt2, ptr->data, NULL, 0); // on recupere les worktree
      }
      liberer(L);
      wt->tab[i].hash = saveWorkTree(
          wt2, absPath); // on recupere le hash final du workfile par recursion
      freeWorkTree(wt2);
      wt->tab[i].mode = getChmod(absPath); // et le mode aussi
      //printf("directory name %s and hash %s mode : %o\n", wf->name, wf->hash, wf->mode);
    }
    free(absPath);
  }
  return blobWorkTree(wt);
}

// permet de restaurer un worktree permettant de recuperer les anciens versions

void restoreWorkTree(WorkTree *wt, char *path) {
  char commande[200];
  sprintf(commande, "mkdir -p %s", path); // cree le repertoire
  system(commande);

  for (int i = 0; i < wt->n; i++) {
    char *hash_path =
        hashToPath(wt->tab[i].hash); // recupere le hash de chaque workfile
    char *buff = concat_paths(path, wt->tab[i].name);
    if (access(hash_path, F_OK) == 0) { // fichier
      cp(buff, hash_path);              // copie le contenu dans buff
      // printf("Dans restore, mode de wt->tab[i] est %o\n", wt->tab[i].mode);
    } else { // repertoire
      strcat(hash_path, ".t");
      // printf("hash_tree dans restore : %s \n", hash_path);
      WorkTree *new_wt =
          ftwts(hash_path); // prend le contenu du fichier hash_path pour
                            // construire un nouveau worktree
      restoreWorkTree(
          new_wt, wt->tab[i].name); // meme processus avec le nouveau worktree
      freeWorkTree(new_wt);
    }
    free(buff);
    free(hash_path);
  }
}

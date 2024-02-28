#include "header.h"
#define TAILLE 10
#define SIZE_COMMIT 10

// 6.1 cree un element
kvp *createKeyVal(char *key, char *val) {
  kvp *new = (kvp *)malloc(sizeof(kvp));
  if (!val && !key)
    return NULL;
  new->key = key ? strdup(key) : NULL;
  new->value = val ? strdup(val) : NULL;
  return new;
}

// libere un element
void freeKeyVal(kvp *kv) {
  if (kv) {
    free(kv->key);
    free(kv->value);
  }
  free(kv);
}

// 6.2 tranforme un element en chaine de caractere
char *kvts(kvp *k) {
  if (!k)
    return NULL;
  char *str = (char *)malloc(100 * sizeof(char));
  snprintf(str, 100, "%s : %s", k->key, k->value);
  return str;
}

// renvoie l'element que represente la chaine str
kvp *stkv(char *str) {
  if (!str)
    return NULL;
  char key[256], val[256];
  sscanf(str, "%s : %s", key, val);
  kvp *new_kv = createKeyVal(key, val);
  return new_kv;
}

// 6.3 initialise un commit
Commit *initCommit() {
  Commit *commit = (Commit *)malloc(sizeof(Commit));
  commit->n = 0;
  commit->size = SIZE_COMMIT;
  commit->T = (kvp **)malloc(SIZE_COMMIT * sizeof(kvp *));
  for (int i = 0; i < commit->size; i++) {
    commit->T[i] = NULL;
  }
  return commit;
}

// 6.4 fonction de hashage du site
unsigned long sdbm(unsigned char *str) {
  unsigned long hash = 0;
  int c;
  while ((c = *(str++)))
    hash = c + (hash << 6) + (hash << 16) - hash;
  return hash;
}

// 6.5
void commitSet(Commit *c, char *key, char *value) {
  unsigned long hash = sdbm((unsigned char *)key) % c->size;
  if (c->n == c->size) {
    printf("commit plein\n");
    return;
  }
  while (c->T[hash]) {
    hash = (hash + 1) % c->size; // par probing lineaire
  }
  c->T[hash] = createKeyVal(key, value);
  (c->n)++;
}

// 6.6 cree un commit en mettant toujours la cle tree
Commit *createCommit(char *hash) {
  Commit *commit = initCommit();
  commitSet(commit, "tree", hash);
  return commit;
}

// 6.7  retourne la valeur(hash) de l'element de la commit ayant comme cle key
char *commitGet(Commit *c, char *key) {
  int i = sdbm((unsigned char *)key) % c->size;
  int cpt = 0;
  while (c->T[i] && cpt < c->size) {
    if (strcmp(c->T[i]->key, key) == 0)
      return c->T[i]->value;
    i = (i + 1) % c->size;
    cpt++;
  }
  return NULL;
}

// libere le commit
void freeCommit(Commit *c) {
  int i = 0;
  while (i < c->size) {
    if (c->T[i])
      freeKeyVal(c->T[i]);
    i++;
  }
  free(c->T);
  free(c);
}

// 6.8 transforme le commit en chaine de caractere
char *cts(Commit *c) {
  char *s = (char *)malloc(c->n * 100 * sizeof(char));
  s[0] = '\0';
  for (int i = 0; i < c->size; i++) {
    if ((c->T[i]) == NULL)
      continue;
    char *ch = kvts(c->T[i]);
    strcat(s, ch);
    strcat(s, "\n");
    free(ch);
  }
  s[strlen(s) - 1] = '\0';
  return s;
}

// transforme une chaine en commit
Commit *stc(char *ch) {
  Commit *c = initCommit();
  char *token = strtok(ch, "\n");
  while (token) {
    // on recupere less caracteres avant \n
    kvp *tmp = stkv(token); // cree l'element
    if (tmp) {
      commitSet(c, tmp->key, tmp->value); // ajout de l'element au commit
      freeKeyVal(tmp);
    }
    token = strtok(NULL, "\n"); // pour ne pas reprendre la chaine deja prise
  }
  return c;
}

// 6.9 ecrit le commit dans le fichier
void ctf(Commit *c, char *file) {
  FILE *f = fopen(file, "w");
  if (!f) {
    printf("Erreur de ctf : Impossible d'ouvrir le fichier %s\n", file);
    return;
  }
  char *s = cts(c);
  fputs(s, f);
  fclose(f);
  free(s);
}

// renvoie le commit du fichier
Commit *ftc(char *file) {
  FILE *source = fopen(file, "r");
  if (source == NULL) {
    printf("Erreur a l'ouverture : le fichier n'existe pas\n");
    return NULL;
  }
  char buffer[256];
  char *ch = malloc(TAILLE * 300 * sizeof(char));
  int debut = 0;
  while (fgets(buffer, 256, source) != NULL) {
    if (debut == 0) { // on copie si c'est la premiere ligne lu
      strcpy(ch, buffer);
      debut = 1;
    } else { // sinon on concatene le reste
      strcat(ch, buffer);
    }
  }
  fclose(source);
  Commit *c = stc(ch); // on prend le commit de la chaine
  free(ch);
  return c;
}

// 6.10 enregistre le commit (meme principe que les autres blobs)
char *blobCommit(Commit *c) {
  char fname[100] = "/tmp/myfileXXXXXX";
  int fd = mkstemp(fname);
  printf("%d/n", fd);
  ctf(c, fname);
  char *hash = sha256file(fname);
  char *ch = hashToFile(hash);
  strcat(ch, ".c");
  cp(ch, fname);
  free(ch);
  return hash;
}

// 7.1
void initRefs() { // on initialise les references s'ils n'existaient pas
  if (!fileExists(".refs")) {
    system("mkdir .refs");
    system("touch .refs/master");
    system("touch .refs/HEAD");
  }
}

// 7.2 met à jour la référence
void createUpdateRef(char *ref_name, char *hash) {
  char buff[256];
  sprintf(buff, ".refs/%s", ref_name);
  if (!fileExists(buff)) {
    sprintf(buff, "touch .refs/%s", ref_name);
    system(buff); // si la reference n'existait pas elle la cree
  }
  sprintf(buff, "echo %s > .refs/%s", hash,
          ref_name); // on ecrie hash dans le reference
  system(buff);
}

// 7.3 supprime la reference
void deleteRef(char *ref_name) {
  char buff[256];
  sprintf(buff, ".refs/%s", ref_name);
  if (!fileExists(buff)) {
    printf("Erreur dans deleteRef: %s n'existe pas", ref_name);
  } else {
    sprintf(buff, "rm .refs/%s", ref_name);
    system(buff);
  }
}

// 7.4 recupere le hash qui etait dans le fichier reference
char *getRef(char *ref_name) {
  if (file_exists(".refs")) {
    List *l = listdir(".refs"); // on recupere la liste des references
    if (searchList(l, ref_name) !=
        NULL) { // on regarde si la ref_name est dedans pour pouvoii recuperer
                // le contenu
      char *buffer = malloc(sizeof(char) * SIZEMAX_CHAR);
      char *ref = malloc(sizeof(char) * (SIZEMAX_CHAR + 10));
      strcpy(ref, ".refs/");
      strcat(ref, ref_name);
      FILE *f = fopen(ref, "r");
      if (fgets(buffer, SIZEMAX_CHAR, f) == NULL) {
        liberer(l);
        free(ref);
        free(buffer);
        return ""; // s'il y'a rien dans le fichier
      } else {
        liberer(l);
        free(ref);
        return buffer;
      }
    } else { // si la reference n'existe pas
      liberer(l);
      return NULL;
    }
  }
  return NULL; // sinon
}

// 7.5 ajoute le fichier ou repertoire dans la zone de preparation
void myGitAdd(char *file_or_folder) {
  WorkTree *wt;
  if (!fileExists(".add")) {
    system("touch .add"); // on cree la zone si elle n'existait pas
    wt = initWorkTree();
  } else {
    wt = ftwts(".add"); // on recupere le wt de la zone
  }
  if (!fileExists(file_or_folder)) {
    printf("Erreur dans myGitadd: %s n'existe pas\n", file_or_folder);
    freeWorkTree(wt);
    return;
  }
  appendWorkTree(wt, file_or_folder, NULL, 0);
  wttf(wt, ".add"); // on recupere le fichier pour le mettre dans la zone
  freeWorkTree(wt);
}

// 7.6 cree un point se saauvegarde comme dans git commit
void myGitCommit(char *branch_name, char *message) {

    if (!file_exists(".refs")) {
        printf("Initialiser d'abord les references du projet!\n");
        return;
    }

    char *path = malloc((SIZEMAX_CHAR + 10) * sizeof(char));
    strcpy(path, ".refs/");
    strcat(path, branch_name);

    List *l = listdir(".refs");

    if (searchList(l, branch_name) == NULL) {
        printf("La branche n'existe pas!\n");
        return;
    }

    char *hashBranch = getRef(branch_name);
    char *hashHEAD = getRef("HEAD");

    if (!((strlen(hashBranch) == 0) && (strlen(hashHEAD) == 0))) {
        if (strcmp(hashBranch, hashHEAD) != 0) {
            printf("HEAD doit pointer sur le dernier commit de la branche!");
            return;
        }
    }

    WorkTree *wt = ftwts(".add");

    char *hashTree = saveWorkTree(wt, "."); //"." signifie le repertoire courant
    
    if(hashTree[strlen(hashTree)-1]=='\n'){
        hashTree[strlen(hashTree)-1]='\0';
    }

    Commit *c = createCommit(hashTree);

    FILE *f = fopen(path, "r");
    char buffer[3* SIZEMAX_CHAR];

    if (strlen(hashBranch) != 0) {
        commitSet(c, "predecessor", hashBranch);
    }

    if (message != NULL) {
        commitSet(c, "message", message);
    }

    commitSet(c, "author", "siwar");

    char *hashCommit = blobCommit(c);

    if(hashCommit[strlen(hashCommit)-1]=='\n'){
        hashCommit[strlen(hashCommit)-1]='\0';
    }
  
    createUpdateRef(branch_name, hashCommit);
    createUpdateRef("HEAD", hashCommit);
    system("rm .add");

    free(path);
    liberer(l);
    free(hashCommit);
    
    free(hashTree);
    freeCommit(c);
    freeWorkTree(wt);
}
	

int file_exists(
    const char *filename) { // regarde si c'est un fichier qui existe
  return (access(filename, F_OK) == 0);
}

// renvoie le format hash d'un commit
char *hashToPathCommit(char *hash) {
  char *tmp = hashToPath(hash);
  tmp[65] = '.';
  tmp[66] = 'c';
  tmp[67] = '\0';
  return tmp;
}
// -> myGit.c

#include "header.h"
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <unistd.h>

// 1.1 et 1.2 dans le terminal


// 1.3 transmet le hash du fichier source à dest
int hashFile(char *source, char *dest) {
  char buff[1000];
  sprintf(buff, "cat %s | sha256sum > %s", source, dest);
  system(buff);
  return 0;
}


// 1.4 met le hash du fichier file dans le fichier temporaire qui est ensuite lu dans ce fichier et retourné
char *sha256file(char *file) {
  static char template[] = "/tmp/myfileXXXXXX";
  char fname[1000];
  strcpy(fname, template);
  int fd = mkstemp(fname);
  hashFile(file, fname);
  char *buff = (char *)malloc(65 * sizeof(char));
  FILE *f = fopen(fname, "r");
  fgets(buff, sizeof(char) * 65, f);
  close(fd);
  fclose(f);
  buff[strlen(buff)]='\0';
  return buff;
}


// 2.1  initialise une liste de cell
List *initList() {
  List *L = (List *)malloc(sizeof(List));
  *L = NULL;
  return L;
}


// 2.2 cree une cellule
Cell *buildCell(char *ch) {
  Cell *cellule = (Cell *)malloc(sizeof(Cell));
  cellule->data = strdup(ch);
  cellule->next = NULL;
  return cellule;
}


// 2.3	insert en tete une cell dans list
void insertFirst(List *L, Cell *C) {
  C->next = *L;
  *L = C;
}


// 2.4 retourne le champ data d'une cell
char *ctos(Cell *c) {
  if (!c)
    return "";
  return c->data;
}


// 2.4 retourne la chaine de concatenation des cell
char *ltos(List *L) {
  Cell *tmp = *L;
  char *res = (char *)malloc(sizeof(char) * 1000);
  strcpy(res, "");
  while (tmp) {
    strcat(res, ctos(tmp));
    strcat(res, "|");
    tmp = tmp->next;
  }
  res[strlen(res) - 1] = '\0';
  return res;
}


// 2.5	retourne l'element de la liste d'indice i
Cell *listGet(List *L, int i) {
  Cell *tmp = *L;
  int count = 0;
  while ((tmp) && (count < i)) {
    count++;
    tmp = tmp->next;
  }
  return tmp;
}


// 2.6 retourne l'element de la liste ayant comme champ data str
Cell *searchList(List *L, char *str) {
  Cell *tmp = *L;
  while ((tmp) && (strcmp(str, tmp->data) != 0)) {
    tmp = tmp->next;
  }
  return tmp;
}


// 2.7 transforme unhe chaine de caractere representant une liste en une liste
List *stol(char *s) {
  List *L = initList();
  char *tmp = strdup(s);
  char *token = strtok(tmp, "|");
  while (token) {
    insertFirst(L, buildCell(token));
    token = strtok(NULL, "|");
  }
  free(tmp);
  return L;
}


// 2.8 ecrit le contenu d'une liste de cell dans un fichier path
void ltof(List *L, char *path) {
  FILE *f = fopen(path, "w");
  Cell *tmp = *L;
  while (tmp) {
    fprintf(f, "%s\n", ctos(tmp));
    tmp = tmp->next;
  }
  fclose(f);
}


//- lis le fichier path et retourne la liste représenté
List *ftol(char *path) {
  FILE *f = fopen(path, "r");
  List *L = initList();
  char buff[1000];
  while (fgets(buff, sizeof(char) * 1000, f)) {
    buff[strlen(buff) - 1] = '\0';
    insertFirst(L, buildCell(buff));
  }
  fclose(f);
  return L;
}


// - libere la mémoire de la liste
void liberer(List *L) {
  Cell *l = *L;
  while (l) {
    Cell *tmp = l->next;
    free(l->data);
    free(l);
    l = tmp;
  }
  free(L);
}

// (facultative) permet d'afficher la liste
void printList(List L) {
  Cell* current = L; // On commence par la tête de la liste
  while (current != NULL) { // On parcourt la liste jusqu'à la fin
    printf("%s\n", current->data); // On affiche le contenu de la cellule courante
    current = current->next; // On passe à la cellule suivante
  }
}

// modifie les autorisations du fichiers
void setMode(int mode, char *path) {
  char buff[100];
  sprintf(buff, "chmod %o %s", mode, path);
  system(buff);
}

// retourne le mode du fichier
int getChmod(const char *path) {
  struct stat ret;

  if (stat(path, &ret) == -1) {
    return -1;
  }
  return (ret.st_mode & S_IRUSR) | (ret.st_mode & S_IWUSR) |
         (ret.st_mode & S_IXUSR) | /*owner*/
         (ret.st_mode & S_IRGRP) | (ret.st_mode & S_IWGRP) |
         (ret.st_mode & S_IXGRP) | /*group*/
         (ret.st_mode & S_IROTH) | (ret.st_mode & S_IWOTH) |
         (ret.st_mode & S_IXOTH); /*other*/
}



// 3.1 retourne la liste des fichierss du repertoire
List *listdir(char *root_dir) {
  List *L = initList();
  DIR *dp = opendir(root_dir);
  struct dirent *ep;
  if (dp) {
    while ((ep = readdir(dp))) {
      insertFirst(L, buildCell(ep->d_name));
    }
    closedir(dp);
  } else
    printf("Erreur ouverture de %s\n", root_dir);
  return L;
}

// regarde si le fichier existe ou pas
struct stat st = {0};

int fileExists(char *file) {
  struct stat buffer;
  return (stat(file, &buffer) == 0) ? 1 : 0;
}


// 3.3 copie le contenu du fichier from vers le fichier to
void cp(char *to, char *from) {
  FILE *fr = fopen(from, "r");
  if (fr) {
    FILE *fw = fopen(to, "w");
    int mode = getChmod(from);
    setMode(mode, to);
    char buff[10000];
    while (fgets(buff, 1000 * sizeof(char), fr)) {
      fprintf(fw, "%s", buff);
      printf("copie de : %s a : %s\nContenu : %s \n", from, to, buff);
    }
    fclose(fr);
    fclose(fw);
  } else
    printf("Erreur d'ouverture du fichier %s\n", from);
}


// 3.4 retourne le chemin du hash
char *hashToPath(char *hash) {
  char *path = (char *)malloc(sizeof(char) * (strlen(hash) + 4));
  snprintf(path, strlen(hash) + 2, "%c%c/%s%c", hash[0], hash[1], hash + 2,'\0');
  return path;
}


// 3.5 enregistre un instantané de fichier
void blobFile(char *file) {
  char *hash = sha256file(file);//recupere le hash du fichier
  char *ch2 = strdup(hash);
  ch2[2] = '\0';
  if (!fileExists(ch2)) {
    char buff[100];
    sprintf(buff, "mkdir %s", ch2);// sui le fichier n'existe pas il cree le repertoire associé
    system(buff);
  }
  char *ch = hashToPath(hash);
  cp(ch, file);// copie le contenu de file dans l'enregistrement du fichier
  free(hash);
  free(ch2);
  free(ch);
}



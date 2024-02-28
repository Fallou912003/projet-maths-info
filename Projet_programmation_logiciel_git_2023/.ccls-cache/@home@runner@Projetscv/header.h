#ifndef HEADER_H
#define HEADER_H

#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h> 
#include <sys/types.h>


#define SIZE 5
#define N 42
#define MAX_FILES 42 
#define Ncommit 42
#define MESSAGE_SIZE 42
#define BLOB_SIZE 42
#define SIZEMAX_CHAR 100

/////////////////////////////////////////
//les structures de base

typedef struct cell {
  char *data;
  struct cell *next;
} Cell;

typedef Cell *List;

typedef struct {
    char* name;
    char* hash;
    int mode;
    } WorkFile;


typedef struct {
    WorkFile* tab;
    int size;
    int n;
   
} WorkTree;


typedef struct key_value_pair{
    char* key;
    char* value;
   
}kvp;
typedef struct hash_table{
    kvp** T;
    int n;
    int size;
} HashTable;
typedef HashTable Commit; 


///////////////////////////////////////////
//le fichier file.c

int hashFile(char *source, char *dest);
char *sha256file(char *file);
List *initList();
Cell *buildCell(char *ch);
void insertFirst(List *L, Cell *C);
char *ctos(Cell *c);
char *ltos(List *L);
Cell *listGet(List *L, int i);
Cell *searchList(List *L, char *str);
List * stol ( char * s );
void ltof(List *L, char *path);
List *ftol(char *path);
void liberer(List *L);
void printList(List L);
List * listdir ( char * root_dir );
int fileExists(char *file);
void cp(char *to, char *from);
char * hashToPath ( char * hash );
void blobFile ( char * file );

///////////////////////////////////////////
//le fichier worktree.c

WorkFile* createWorkFile(char* name);
void freeWorkFile(WorkFile* wf);
char* wfts(WorkFile* wf);
WorkFile* stwf(char* ch);
WorkTree* initWorkTree();
void printWorkTree(WorkTree *wt);
int inWorkTree(WorkTree* wt, char* name);
int appendWorkTree(WorkTree* wt, char* name, char* hash, int mode) ;
char* wtts(WorkTree* wt);
WorkTree* stwt(char* str);
int wttf(WorkTree* wt, char* file);
WorkTree* ftwts(char* file);
void freeWorkTree(WorkTree *wt) ;
char* hashToFile(char* hash);
char* blobWorkTree(WorkTree* wt);
int isDirectory(const char *path);
char *concat_paths(char *path1, char *path2);
char* saveWorkTree(WorkTree* wt, char* path);
void restoreWorkTree(WorkTree* wt, char* path);
int getChmod(const char *path);

/////////////////////////////////////////////////
//le fichier commit.c

kvp* createKeyVal(char* key, char* val);
void freeKeyVal(kvp* kv);
char* kvts(kvp* k);
kvp* stkv(char* str);
Commit* initCommit();
void freeCommit(Commit* c);
unsigned long sdbm(unsigned char *str) ;
void commitSet(Commit* c, char* key, char* value);
Commit* createCommit(char* hash);
char* commitGet(Commit* c, char* key);
char* cts(Commit* c);
Commit* stc(char* ch);
Commit* ftc(char* file);
void ctf(Commit* c, char* file);
char* blobCommit(Commit* c);
char* hashToPathCommit(char*hash);
int file_exists(const char *filename);
void initRefs();
void createUpdateRef(char* ref_name, char* hash);
void deleteRef(char* ref_name);
char* getRef(char* ref_name);
void createFile(char* file);
void myGitAdd(char* file_or_folder);
void createRef(char* ref_name , char* hash);
char* blobCommit(Commit* c);
void myGitCommit(char *branch_name, char *message);
void setMode(int mode, char *path);

//////////////////////////////////////
//le fichier branche.c

void initBranch() ;
int branchExists(char *branch);
void createBranch(char *branch) ;
char *getCurrentBranch() ;
void printBranch(char *branch);
List *branchList(char *branch);
List *getAllCommits() ;
void restoreCommit(char *hash_commit) ;
void myGitCheckoutBranch(char *branch) ;
List *filterList(List *L, char *pattern);
void myGitCheckoutCommit(char *pattern);


//////////////////////////////////////////////
//le fichier merge.c

WorkTree *mergeWorkTrees(WorkTree *wt1, WorkTree *wt2, List **conflicts);
List *merge(char *remote_branch, char *message);
void createDeletionCommit(char *branch, List *conflicts, char *message);


#endif

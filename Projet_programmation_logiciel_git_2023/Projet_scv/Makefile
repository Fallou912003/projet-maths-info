GCC_FLAGS=-Wall -g 
EXEC= main myGit 

all: $(EXEC)

clean:
	rm -f *.o $(EXEC) *~

.c.o:   
	gcc $(GCC_FLAGS) -c $*.c

main: main.o file.o branche.o merge.o commit.o workfile.o header.h
	gcc ${GCC_FLAGS} -o $@ $^
	
myGit: myGit.o file.o branche.o merge.o commit.o workfile.o header.h
	gcc ${GCC_FLAGS} -o $@ $^

file: file.o header.h
	gcc ${GCC_FLAGS} -o $@ $^
	
branche: branche.o header.h
	gcc ${GCC_FLAGS} -o $@ $^
	
merge: merge.o header.h
	gcc ${GCC_FLAGS} -o $@ $^
	
commit: commit.o header.h
	gcc ${GCC_FLAGS} -o $@ $^

workfile: workfile.o header.h
	gcc ${GCC_FLAGS} -o $@ $^


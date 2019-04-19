#include <stdio.h>
#include <assert.h>
#include "klee/klee.h"

int even(){
	int a,b,c;
	klee_make_symbolic(&a, sizeof(a), "a");
	klee_make_symbolic(&b, sizeof(b), "b");
	klee_make_symbolic(&c, sizeof(c), "c");
	int x = 0, y = 0, z = 0;

	if(a) x = -2;	
	if(b < 5) {
		if(! a && c) { y = 1; }
		z = 2;
	}

	klee_assert(x+y+z != 3);
	return 1;

}

int main(int argc, char* argv[]){
	int x;
	return even();
}
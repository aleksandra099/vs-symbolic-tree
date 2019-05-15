#include <klee/klee.h>

int primer(int a0, int a1,int a2, int a3, int a4)
{
	int k, n = 0;

	klee_make_symbolic(&a0, sizeof(a0), "a0");
	klee_make_symbolic(&a1, sizeof(a1), "a1");
	klee_make_symbolic(&a2, sizeof(a2), "a2");
	klee_make_symbolic(&a3, sizeof(a3), "a3");
	klee_make_symbolic(&a4, sizeof(a4), "a4");

	if (a0 > 0)
		a0 = 1;
	else
		a0 = -1;
	if (a1 > 0)
		a1 = 1;
	else
		a1 = -1;
	if (a2 > 0)
		a2 = 1;
	else
		a2 = -1;
	if (a3 > 0)
		a3 = 1;
	else
		a3 = -1;
	if (a4 > 0)
		a4 = 1;
	else
		a4 = -1;

	n = (a0 + a1 + a2 + a3 + a4);

	return 1;
}



int main(int argc, char* argv[]) {
  int a0, a1, a2, a3, a4;

  klee_make_symbolic(&a0, sizeof(int),"a0");
  klee_make_symbolic(&a1, sizeof(int),"a1");
  klee_make_symbolic(&a2, sizeof(int),"a2");
  klee_make_symbolic(&a3, sizeof(int),"a3");
  klee_make_symbolic(&a4, sizeof(int),"a4");


  return primer( a0, a1, a2, a3, a4);
}
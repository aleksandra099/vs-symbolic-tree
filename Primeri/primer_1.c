#include <stdio.h>
#include <assert.h>
#include <klee/klee.h>

void nebitno(int a, int b, int c) {
    int x = 0, y = 0, z = 0;

    if (a) {
        x = -2;
    }
    if (b < 5) {
        if (!a && c) {
            y = 1;
        }
        z = 2;
    }

    klee_assert(x + y + z != 3);
}

int main(int argc, char* argv[]) {
    int a, b, c;
    klee_make_symbolic(&a, sizeof(int), "a");
    klee_make_symbolic(&b, sizeof(int), "b");
    klee_make_symbolic(&c, sizeof(int), "c");
    // b = 0;
    // c = 0;
  
    nebitno(a, b, c);
}


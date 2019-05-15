#include <stdio.h>
#include <assert.h>
#include <klee/klee.h>

int isPrime(int x)
{
  for (int i = 2; i*i <= x; i++)
  {
    if (x % i == 0)
    {
      return 0;
    }
  }
  return 1;
}

int main()
{
  int x;
  
  klee_make_symbolic(&x, sizeof(x), "x");
		
  if(x>80) 
     return 0;
  int no = isPrime(x);

  return 0;
}

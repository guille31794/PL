#include "stdio.h"

int main(int argc, char const *argv[])
{
    int a=1, **p = &a;
    printf("%d", *p);
}

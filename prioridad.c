#include "stdio.h"

/*int max(int x, int y)
{
    int max;
    if (x < y)
        max = y;
    else
        max = x;
    return max;
}*/

int max(int x, int y, int z)
{
    int max;
    if(x > y && x > z)
        max = x;
    else if(y > x && y > z)
        max = y;
    else if(z > x && z > y)
        max = z;

    return max;
}

int main(int argc, char const *argv[])
{
    int a, b, c, res;

    printf("Introduzca un numero entero\n");
    scanf("%d", &a);
    printf("Introduzca otro número entero\n");
    scanf("%d", &b);
    printf("Introduzca otro número entero\n");
    scanf("%d", &c);
    res = max(a,b,c);
    printf("El maximo de %d, %d y %d es %d",a,b,c,res);
    return 0;
}

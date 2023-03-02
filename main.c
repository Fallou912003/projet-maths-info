#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "polynome.h"

int main() {
    
    Polynome* p1 = initialiser_polynome();
    Polynome* p2 = initialiser_polynome();
    Polynome* p3 = katsubara(p1,p2);
    Polynome* p4 = mult_naive(p1,p2);
    
    printf("mult par katsubara : "); affiche_polynome(p3);
    printf("mult naïve : "); affiche_polynome(p4);

    detruire_polynome(p1);
    detruire_polynome(p2);
    detruire_polynome(p3);
    detruire_polynome(p4);
    
    return 0;
}

#include <stdlib.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int search() {

    int legal_moves[MAX_GEN_MOVES];
    int i = 0;

    for(int m = 0; m < n_moves[ply]; m++) {
        if(make_move(m)) {
            legal_moves[i++] = m;
            take_back();
        }
    }

    if(i) {
        return legal_moves[rand() % i];
    }
    return -1;
}
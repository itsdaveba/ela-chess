#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "protos.h"

int main()
{
    char fen[] = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1 b kq g3 0 1";
    if (set_board(fen))
    {
        print_board();
        if (strcmp(fen, get_fen())) {
            printf("ERROR\n");
        }
    }
    return 0;
}
#include <stdio.h>
#include "defs.h"
#include "data.h"

void print_board()
{
    printf("\n  A B C D E F G H");
    for (int s = 0; s < 64; s++)
    {
        if (FILE(board[s]) == FILE_A)
        {
            printf("\n%d", RANK(board[s]) + 1);
        }
        if (color[board[s]] == WHITE)
        {
            printf(" %c", piece_to_char[piece[board[s]]]);
        }
        else
        {
            printf(" %c", piece_to_char[piece[board[s]]] | ' ');
        }
    }
    printf("\n\n");
}
#include <stdlib.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

move_t search()
{
    move_t move;

    shuffle_moves();

    for (int m = 0; m < n_moves[0]; m++)
    {
        if (make_move(move_list[0][m]))
        {
            take_back();
            return move_list[0][m];
        }
    }

    move.type = NO_MOVE;
    return move;
}

void shuffle_moves()
{
    int i, j;
    move_t temp;

    for (i = n_moves[0] - 1; i > 0; i--)
    {
        j = rand() % (i + 1);
        temp = move_list[0][i];
        move_list[0][i] = move_list[0][j];
        move_list[0][j] = temp;
    }
}
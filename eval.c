#include "defs.h"
#include "data.h"

int evaluate()
{
    int value = 0;

    for (int s = 0; s < 64; s++)
    {
        if (color[s] == WHITE)
        {
            if (piece[s] != KING)
            {
                value += piece_value[piece[s]];
            }
            value += piece_table[piece[s]][s];
        }
        else if (color[s] == BLACK)
        {
            if (piece[s] != KING)
            {
                value -= piece_value[piece[s]];
            }
            value -= piece_table[piece[s]][bigend_rank[s]];
        }
    }

    if (side == BLACK)
    {
        value = -value;
    }

    return value;
}
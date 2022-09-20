#include <stdlib.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

move_t search(int search_depth)
{
    int score;
    int alpha = -10000;
    int beta = 10000;

    for (int m = 0; m < n_moves[0]; m++)
    {
        if (make_move(move_list[0][m]))
        {
            score = -negamax(-beta, -alpha, search_depth - 1);
            take_back();
            if (score >= beta)
            {
                return move_list[0][m];
            }
            if (score > alpha)
            {
                alpha = score;
                move_list[0][0] = move_list[0][m];
            }
        }
    }

    return move_list[0][0];
}

int negamax(int alpha, int beta, int depth)
{
    if (depth == 0)
    {
        return evaluate();
    }

    int score;

    gen_moves();

    for (int m = 0; m < n_moves[ply]; m++)
    {
        if (make_move(move_list[ply][m]))
        {
            score = -negamax(-beta, -alpha, depth - 1);
            take_back();
            if (score >= beta)
            {
                return beta;
            }
            if (score > alpha)
            {
                alpha = score;
            }
        }
    }

    return alpha;
}

void shuffle_moves(int ply)
{
    int i, j;
    move_t temp;

    for (i = n_moves[ply] - 1; i > 0; i--)
    {
        j = rand() % (i + 1);
        temp = move_list[ply][i];
        move_list[ply][i] = move_list[ply][j];
        move_list[ply][j] = temp;
    }
}
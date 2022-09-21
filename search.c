#include <stdio.h>
#include <stdlib.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

void search(int search_depth, bool post)
{
    int score;

    nodes = 0;

    for (int depth = 1; depth <= search_depth; depth++)
    {
        score = negamax(-100000, 100000, depth);
        if (post)
        {
            printf("%d %d %d %d", depth, score, 0, nodes);
            for (int d = 0; d < depth; d++)
            {
                printf(" %s", move_to_lan(pv[0][d]));
            }
            printf("\n");
        }
        if (abs(score) >= 100000 - MAX_DEPTH)
        {
            break;
        }
    }
}

int negamax(int alpha, int beta, int depth)
{
    int score;
    bool legal_move = FALSE;

    if (depth == 0)
    {
        nodes++;
        return evaluate();
    }

    if (ply != 0)
    {
        gen_moves();
    }

    for (int m = 0; m < n_moves[ply]; m++)
    {
        if (make_move(move_list[ply][m]))
        {
            if (!legal_move)
            {
                legal_move = TRUE;
            }
            score = -negamax(-beta, -alpha, depth - 1);
            take_back();
            if (score >= beta)
            {
                return beta;
            }
            if (score > alpha)
            {
                alpha = score;
                pv[ply][ply] = move_list[ply][m];
                for (int p = ply + 1; p < ply + depth; p++)
                {
                    pv[ply][p] = pv[ply + 1][p];
                }
            }
        }
    }

    if (!legal_move)
    {
        if (in_check(side))
        {
            return -100000 + ply;
        }
        else
        {
            return 0;
        }
    }

    return alpha;
}

void shuffle_moves()
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
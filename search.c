#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

move_t search(int search_time, int search_depth, bool post)
{
    int score;
    line_t pv;

    ply = 0;
    nodes = 0;
    pv.best[0].type = NO_MOVE;

    if (search_depth == 0)
    {
        int n_moves;
        move_t move_list[MAX_GEN_MOVES];
        n_moves = gen_moves(move_list, FALSE);
        shuffle_moves(n_moves, move_list);
        for (int m = 0; m < n_moves; m++)
        {
            if (make_move(move_list[m]))
            {
                take_back();
                return move_list[m];
            }
        }
    }

    for (int depth = 1; depth <= search_depth; depth++)
    {
        score = negamax(MIN_SCORE, MAX_SCORE, depth, &pv);
        if (post && (pv.best[0].type & NO_MOVE) == 0)
        {
            printf("%d %d %d %llu", depth, score, 0, nodes);
            for (int d = 0; d < pv.depth; d++)
            {
                printf(" %s", move_to_lan(pv.best[d]));
            }
            printf("\n");
        }
        if (abs(score) > MATE_THRESHOLD)
        {
            break;
        }
    }

    return pv.best[0];
}

int negamax(int alpha, int beta, int depth, line_t *pline)
{
    int score;
    line_t line;
    bool legal_move;
    int n_moves;
    move_t move_list[MAX_GEN_MOVES];

    if (depth == 0)
    {
        return quiesce(alpha, beta, pline);
    }

    pline->depth = 0;
    legal_move = FALSE;
    n_moves = gen_moves(move_list, FALSE);

    for (int m = 0; m < n_moves; m++)
    {
        if (make_move(move_list[m]))
        {
            if (!legal_move)
            {
                legal_move = TRUE;
            }
            score = -negamax(-beta, -alpha, depth - 1, &line);
            take_back();
            if (score >= beta)
            {
                return beta;
            }
            if (score > alpha)
            {
                alpha = score;
                if (ply < MAX_PV_LENGTH)
                {
                    pline->best[0] = move_list[m];
                    memcpy(pline->best + 1, line.best, line.depth * sizeof(move_t));
                    pline->depth = line.depth + 1;
                }
            }
        }
    }

    if (!legal_move)
    {
        if (in_check(side))
        {
            return MIN_SCORE + ply;
        }
        else
        {
            return DRAW_SCORE;
        }
    }

    return alpha;
}

int quiesce(int alpha, int beta, line_t *pline)
{
    int score;
    int n_moves;
    line_t line;
    move_t move_list[MAX_GEN_MOVES];

    nodes++;
    pline->depth = 0;
    score = evaluate();

    if (score >= beta)
    {
        return beta;
    }
    if (score > alpha)
    {
        alpha = score;
    }

    n_moves = gen_moves(move_list, TRUE);

    for (int m = 0; m < n_moves; m++)
    {
        if (make_move(move_list[m]))
        {
            score = -quiesce(-beta, -alpha, &line);
            take_back();
            if (score >= beta)
            {
                return beta;
            }
            if (score > alpha)
            {
                alpha = score;
                if (ply < MAX_PV_LENGTH)
                {
                    pline->best[0] = move_list[m];
                    memcpy(pline->best + 1, line.best, line.depth * sizeof(move_t));
                    pline->depth = line.depth + 1;
                }
            }
        }
    }

    return alpha;
}

void shuffle_moves(int n_moves, move_t *move_list)
{
    int i, j;
    move_t temp;

    for (i = n_moves - 1; i > 0; i--)
    {
        j = rand() % (i + 1);
        temp = move_list[i];
        move_list[i] = move_list[j];
        move_list[j] = temp;
    }
}
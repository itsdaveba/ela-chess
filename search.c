#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include <sys/time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

move_t search(bool post, bool book)
{
    static move_t move;

    int score;
    bool stop;
    line_t pv;

    if (book)
    {
        move = book_move();
        if ((move.type & NO_MOVE) == 0)
        {
            return move;
        }
    }

    ply = 0;
    nodes = 0;
    pv.best[0].type = NO_MOVE;
    gettimeofday(&start, NULL);

    stop = setjmp(env);
    if (stop)
    {
        while (ply > 0)
        {
            take_back();
        }
        return move;
    }

    if (search_depth == 0 || search_time == 0)
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
        move = pv.best[0];
        if (post && (pv.best[0].type & NO_MOVE) == 0)
        {
            gettimeofday(&now, NULL);
            printf("%d %d %d %llu", depth, score, time_diff(start, now), nodes);
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

    if (ply == 0)
    {
        shuffle_moves(n_moves, move_list);
    }

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
    if ((nodes & 0xFFFF) == 0)
    {
        gettimeofday(&now, NULL);
        if (time_diff(start, now) >= search_time)
        {
            longjmp(env, TRUE);
        }
    }

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

int time_diff(struct timeval start, struct timeval now)
{
    int diff_sec = now.tv_sec - start.tv_sec;
    int diff_usec = now.tv_usec - start.tv_usec;
    return diff_sec * 100 + diff_usec / 10000;
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
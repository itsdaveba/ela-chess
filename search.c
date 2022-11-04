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

    if (book)
    {
        move = book_move();
        if (!(move.bytes.type & NO_MOVE))
        {
            return move;
        }
    }

    ply = 0;
    nodes = 0;
    move.bytes.type = NO_MOVE;
    pv[0][0].bytes.type = NO_MOVE;
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
        gen_t move_list[MAX_GEN_MOVES];
        n_moves = gen_moves(move_list, FALSE);
        shuffle_moves(n_moves, move_list);
        for (int m = 0; m < n_moves; m++)
        {
            if (make_move(move_list[m].move))
            {
                take_back();
                return move_list[m].move;
            }
        }
    }

    memset(heuristic, 0, sizeof(heuristic));
    for (int depth = 1; depth <= search_depth; depth++)
    {
        score = negamax(MIN_SCORE, MAX_SCORE, depth);
        move = pv[0][0];
        if (post && !(pv[0][0].bytes.type & NO_MOVE))
        {
            gettimeofday(&now, NULL);
            printf("%d %d %d %llu", depth, score, time_diff(start, now), nodes);
            for (int d = 0; d < pv_length[0]; d++)
            {
                printf(" %s", move_to_lan(pv[0][d]));
            }
            printf("\n");
        }
        if (abs(score) > MATE_THRESHOLD)
        {
            break;
        }
    }

    return pv[0][0];
}

int negamax(int alpha, int beta, int depth)
{
    int score;
    bool legal_move;
    int node_type;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];
    bool check = in_check(side);

    nodes++;
    check_time();

    if (check)
    {
        depth++;
    }

    if (depth == 0)
    {
        return quiesce(alpha, beta);
    }

    if (ply < MAX_PV_LENGTH)
    {
        pv_length[ply] = ply;
    }
    legal_move = FALSE;
    node_type = ALL_NODE;
    n_moves = gen_moves(move_list, FALSE);

    if (ply == 0)
    {
        shuffle_moves(n_moves, move_list);
    }

    move_t best;
    best.bytes.type = NO_MOVE;
    score = probe_hash(alpha, beta, depth, &best);
    if (score != NULL_SCORE)
    {
        return score;
    }
    follow_hash(best, n_moves, move_list);

    for (int m = 0; m < n_moves; m++)
    {
        sort_move(m, n_moves, move_list);
        if (make_move(move_list[m].move))
        {
            if (!legal_move)
            {
                legal_move = TRUE;
            }
            score = -negamax(-beta, -alpha, depth - 1);
            take_back();
            if (score >= beta)
            {
                if (!(move_list[m].move.bytes.type & CAPTURE))
                {
                    heuristic[move_list[m].move.bytes.from][move_list[m].move.bytes.to] += depth * depth;
                }
                store_hash(alpha, depth, CUT_NODE, move_list[m].move);
                return beta;
            }
            if (score > alpha)
            {
                alpha = score;
                if (node_type != PV_NODE)
                {
                    node_type = PV_NODE;
                }
                best = move_list[m].move;
                if (ply < MAX_PV_LENGTH)
                {
                    pv[ply][ply] = move_list[m].move;
                    if (ply + 1 < MAX_PV_LENGTH)
                    {
                        for (int p = ply + 1; p < pv_length[ply + 1]; p++)
                        {
                            pv[ply][p] = pv[ply + 1][p];
                        }
                        pv_length[ply] = pv_length[ply + 1];
                    }
                    else
                    {
                        pv_length[ply] = MAX_PV_LENGTH;
                    }
                }
            }
        }
    }

    if (!legal_move)
    {
        if (check)
        {
            alpha = MIN_SCORE + ply;
        }
        else
        {
            alpha = DRAW_SCORE;
        }
    }

    store_hash(alpha, depth, node_type, best);
    return alpha;
}

int quiesce(int alpha, int beta)
{
    int score;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];

    nodes++;
    check_time();

    if (ply < MAX_PV_LENGTH)
    {
        pv_length[ply] = ply;
    }
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
        sort_move(m, n_moves, move_list);
        if (make_move(move_list[m].move))
        {
            score = -quiesce(-beta, -alpha);
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
                    pv[ply][ply] = move_list[m].move;
                    if (ply + 1 < MAX_PV_LENGTH)
                    {
                        for (int p = ply + 1; p < pv_length[ply + 1]; p++)
                        {
                            pv[ply][p] = pv[ply + 1][p];
                        }
                        pv_length[ply] = pv_length[ply + 1];
                    }
                    else
                    {
                        pv_length[ply] = MAX_PV_LENGTH;
                    }
                }
            }
        }
    }

    return alpha;
}

void follow_hash(move_t hash_move, int n_moves, gen_t *move_list)
{
    if (!(hash_move.bytes.type & NO_MOVE))
    {
        for (int m = 0; m < n_moves; m++)
        {
            if (move_list[m].move.id == hash_move.id)
            {
                move_list[m].score = __INT_MAX__ - 1;
                break;
            }
        }
    }
}

int time_diff(struct timeval start, struct timeval now)
{
    int diff_sec = now.tv_sec - start.tv_sec;
    int diff_usec = now.tv_usec - start.tv_usec;
    return diff_sec * 100 + diff_usec / 10000;
}

void check_time()
{
    if (!(nodes & 0xFFFF))
    {
        gettimeofday(&now, NULL);
        if (time_diff(start, now) >= search_time)
        {
            longjmp(env, TRUE);
        }
    }
}

void swap_moves(gen_t *move_x, gen_t *move_y)
{
    gen_t temp = *move_x;
    *move_x = *move_y;
    *move_y = temp;
}

void shuffle_moves(int n_moves, gen_t *move_list)
{
    int x, y;

    for (x = n_moves - 1; x > 0; x--)
    {
        y = rand() % (x + 1);
        swap_moves(&move_list[x], &move_list[y]);
    }
}

void sort_move(int m, int n_moves, gen_t *move_list)
{
    int max_i = m;
    for (int i = m + 1; i < n_moves; i++)
    {
        if (move_list[i].score > move_list[max_i].score)
        {
            max_i = i;
        }
    }
    if (max_i != m)
    {
        swap_moves(&move_list[max_i], &move_list[m]);
    }
}
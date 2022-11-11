#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include <sys/time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

// Search root
move_t search(bool post, bool book)
{
    static move_t move;

    int score;
    int alpha;
    int beta;
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
    alpha = MIN_SCORE;
    beta = MAX_SCORE;
    move.bytes.type = NO_MOVE;
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

    for (int depth = 1; depth <= search_depth;)
    {
        score = negamax(alpha, beta, depth);
        move = transp_table[hash % TRANSP_SIZE].best_move;
        if (score <= alpha && score != MIN_SCORE)
        {
            alpha = MIN_SCORE;
            continue;
        }
        if (score >= beta && score != MAX_SCORE)
        {
            beta = MAX_SCORE;
            continue;
        }
        alpha = score - 50;
        beta = score + 50;
        if (post && (move.bytes.type & NO_MOVE) == 0)
        {
            gettimeofday(&now, NULL);
            printf("%d %d %d %llu", depth, score, time_diff(start, now), nodes);
            print_pv();
            printf("\n");
        }
        if (abs(score) > MATE_THRESHOLD)
        {
            break;
        }
        depth++;
    }

    return move;
}

// Negamax search node
int negamax(int alpha, int beta, int depth)
{
    int score;
    bool legal_move;
    int node_type;
    move_t best_move;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];
    bool check = in_check(side);

    if (check)
    {
        depth++;
    }

    best_move.bytes.type = NO_MOVE;
    if (probe_hash(alpha, beta, depth, &score, &best_move))
    {
        return score;
    }

    if (depth == 0)
    {
        return quiesce(alpha, beta);
    }

    nodes++;
    check_time();

    legal_move = FALSE;
    node_type = ALL_NODE;
    n_moves = gen_moves(move_list, FALSE);

    if (ply == 0)
    {
        shuffle_moves(n_moves, move_list);
    }

    if (!(best_move.bytes.type & NO_MOVE))
    {
        score_move(best_move, __INT_MAX__, n_moves, move_list);
    }

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
                best_move = move_list[m].move;
                if (!(best_move.bytes.type & CAPTURE))
                {
                    heuristic[best_move.bytes.from][best_move.bytes.to] += depth * depth;
                }
                store_hash(beta, depth, CUT_NODE, best_move);
                return beta;
            }
            if (score > alpha)
            {
                alpha = score;
                if (node_type != PV_NODE)
                {
                    node_type = PV_NODE;
                }
                best_move = move_list[m].move;
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

    store_hash(alpha, depth, node_type, best_move);
    return alpha;
}

// Quiesce search node
int quiesce(int alpha, int beta) // TODO: transposition table for quiesce search
{
    int score;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];

    nodes++;
    check_time();

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
            }
        }
    }

    return alpha;
}

// Print principal variation
void print_pv()
{
    transp_t *transp = &transp_table[hash % TRANSP_SIZE];

    if (repetition() < 3)
    {
        if ((((u64)transp->hash_high << 8) | transp->hash_mid) == hash >> 24)
        {
            if (transp->node_type == PV_NODE && make_move(transp->best_move))
            {
                printf(" %s", move_to_lan(transp->best_move));
                print_pv();
                take_back();
            }
        }
    }
}

// Get time from start of search
int time_diff(struct timeval start, struct timeval now)
{
    int diff_sec = now.tv_sec - start.tv_sec;
    int diff_usec = now.tv_usec - start.tv_usec;
    return diff_sec * 100 + diff_usec / 10000;
}

// Check when time is up
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

// Score single move
void score_move(move_t move, int score, int n_moves, gen_t *move_list)
{
    for (int m = 0; m < n_moves; m++)
    {
        if (move_list[m].move.id == move.id)
        {
            move_list[m].score = score;
            break;
        }
    }
}

// Swap two moves
void swap_moves(gen_t *move_x, gen_t *move_y)
{
    gen_t temp = *move_x;
    *move_x = *move_y;
    *move_y = temp;
}

// Shuffle moves randomly
void shuffle_moves(int n_moves, gen_t *move_list)
{
    int x, y;

    for (x = n_moves - 1; x > 0; x--)
    {
        y = rand() % (x + 1);
        swap_moves(&move_list[x], &move_list[y]);
    }
}

// Insertion sort from best to worst
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
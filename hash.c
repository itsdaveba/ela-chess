#include <stdlib.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

u64 rand_hash()
{
    u64 rand_num;

    rand_num = rand();
    rand_num ^= (u64)rand() << 15;
    rand_num ^= (u64)rand() << 30;
    rand_num ^= (u64)rand() << 45;
    rand_num ^= (u64)rand() << 60;

    return rand_num;
}

void init_hash()
{
    for (int s = 0; s < 64; s++)
    {
        for (int p = PAWN; p <= KING; p++)
        {
            hash_table[s][p][BLACK] = rand_hash();
            hash_table[s][p][WHITE] = rand_hash();
        }
    }
}

void set_hash()
{
    hash = 0;

    for (int s = 0; s < 64; s++)
    {
        if (piece[s] != EMPTY)
        {
            hash ^= hash_table[s][piece[s]][color[s]];
        }
    }

    if (side == BLACK)
    {
        hash ^= hash_table[A8][PAWN][WHITE];
    }

    hash ^= hash_table[(castling + A8) & H8][PAWN][BLACK];

    if (passant != -1)
    {
        if (side == WHITE)
        {
            if ((FILE(passant) != FILE_A && piece[passant + DOWN_LEFT] == PAWN && color[passant + DOWN_LEFT] == WHITE) ||
                (FILE(passant) != FILE_H && piece[passant + DOWN_RIGHT] == PAWN && color[passant + DOWN_RIGHT] == WHITE))
            {
                hash ^= hash_table[FILE(passant)][PAWN][WHITE];
            }
        }
        else
        {
            if ((FILE(passant) != FILE_A && piece[passant + UP_LEFT] == PAWN && color[passant + UP_LEFT] == BLACK) ||
                (FILE(passant) != FILE_H && piece[passant + UP_RIGHT] == PAWN && color[passant + UP_RIGHT] == BLACK))
            {
                hash ^= hash_table[FILE(passant)][PAWN][WHITE];
            }
        }
    }
}

void store_hash(int score, int depth, int node_type, move_t best_move)
{
    transp_t *transp = &transp_table[hash % TRANSP_SIZE];

    transp->hash_high = hash >> 32;
    transp->hash_mid = hash >> 24;
    transp->score = score;
    transp->depth = depth;
    transp->node_type = node_type;
    if (node_type != ALL_NODE)
    {
        transp->best_move = best_move;
    }
    else
    {
        transp->best_move.bytes.type = NO_MOVE;
    }
}

bool probe_hash(int alpha, int beta, int depth, int *score, move_t *best_move)
{
    transp_t transp = transp_table[hash % TRANSP_SIZE];

    if ((((u64)transp.hash_high << 8) | transp.hash_mid) == hash >> 24)
    {
        if (transp.depth >= depth)
        {
            if (transp.node_type == PV_NODE)
            {
                *score = transp.score;
                return TRUE;
            }
            if (transp.node_type == CUT_NODE && transp.score >= beta)
            {
                *score = beta;
                return TRUE;
            }
            if (transp.node_type == ALL_NODE && transp.score <= alpha)
            {
                *score = alpha;
                return TRUE;
            }
        }
        *best_move = transp.best_move;
    }

    return FALSE;
}
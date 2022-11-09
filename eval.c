#include "defs.h"
#include "data.h"
#include "protos.h"

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

int see(int square, int side)
{
    int score;
    int capture;
    int value = 0;
    int from = attacker(square, side, 0);
    move_t move = history[ply - 1].move;

    if (move.bytes.type & PROMOTION && move.bytes.to == square)
    {
        capture = PAWN;
    }
    else
    {
        capture = piece[square];
    }

    for (int i = 1; from != -1; i++)
    {
        move = gen_capture(from, square, QUEEN);
        if (make_move(move))
        {
            score = piece_value[capture] - see(square, side ^ 1);
            take_back();
            if (score > -piece_value[PAWN])
            {
                value = score;
            }
            break;
        }
        from = attacker(square, side, i);
    }

    return value;
}

int see_capture(move_t move)
{
    int capture;
    int value = 0;

    if (move.bytes.type & EP_CAPTURE)
    {
        capture = PAWN;
    }
    else
    {
        capture = piece[move.bytes.to];
    }

    if (make_move(move))
    {
        value = piece_value[capture] - see(move.bytes.to, side);
        take_back();
    }

    return value;
}
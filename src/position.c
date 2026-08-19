#include <stdio.h>
#include <string.h>
#include "position.h"

int perft(Position *position, int depth)
{
    return 0;
}

void display_position(Position *position)
{
    printf("Position\n");
}

void get_fen(Position *position, char *fen)
{
}

void reset_position(Position *position, char *fen)
{
    char board[72];
    char side;
    char castling[5];
    char epsquare[3];
    int halfmove;
    int fullmove;
    sscanf(fen, "%s %c %s %s %d %d", board, &side, castling, epsquare, &halfmove, &fullmove);

    if (side == 'w')
        position->side = WHITE;
    else if (side == 'b')
        position->side = BLACK;
}

void make_move(Position *position, Move move)
{
}
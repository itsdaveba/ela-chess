#ifndef POSITION_H
#define POSITION_H

#include "move.h"

#define MAX_FEN_LENGTH 128
#define STARTING_POSITION_FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

typedef enum
{
    WHITE,
    BLACK
} Color;

typedef struct
{
    Color side;
    int eval;
} Position;

int perft(Position *position, int depth);

void display_position(Position *position);
void get_fen(Position *position, char *fen);
void reset_position(Position *position, char *fen);
void make_move(Position *position, Move move);

#endif
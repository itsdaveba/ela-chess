#include "defs.h"

int piece[64] = {
    ROOK  , KNIGHT, BISHOP, QUEEN , KING  , BISHOP, KNIGHT, ROOK  ,
    PAWN  , PAWN  , PAWN  , PAWN  , PAWN  , PAWN  , PAWN  , PAWN  ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    PAWN  , PAWN  , PAWN  , PAWN  , PAWN  , PAWN  , PAWN  , PAWN  ,
    ROOK  , KNIGHT, BISHOP, QUEEN , KING  , BISHOP, KNIGHT, ROOK
};
int color[64] = {
    WHITE , WHITE , WHITE , WHITE , WHITE , WHITE , WHITE , WHITE ,
    WHITE , WHITE , WHITE , WHITE , WHITE , WHITE , WHITE , WHITE ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY , EMPTY ,
    BLACK , BLACK , BLACK , BLACK , BLACK , BLACK , BLACK , BLACK ,
    BLACK , BLACK , BLACK , BLACK , BLACK , BLACK , BLACK , BLACK
};

char piece_to_char[7] = {'.', 'P', 'R', 'N', 'B', 'Q', 'K'};

int board[64] = {
    56, 57, 58, 59, 60, 61, 62, 63,
    48, 49, 50, 51, 52, 53, 54, 55,
    40, 41, 42, 43, 44, 45, 46, 47,
    32, 33, 34, 35, 36, 37, 38, 39,
    24, 25, 26, 27, 28, 29, 30, 31,
    16, 17, 18, 19, 20, 21, 22, 23,
     8,  9, 10, 11, 12, 13, 14, 15,
     0,  1,  2,  3,  4,  5,  6,  7 
};
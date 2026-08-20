#include <stdio.h>
#include <string.h>
#include "position.h"
#include "board.h"

const uint64_t HASH_SIDE[2] = {0, 0};

int perft(Position *position, int depth)
{
    return 0;
}

void init_position(Position *position, char *fen)
{
    char board_str[72];
    char side_chr;
    char castling_str[5];
    char epsquare_str[3];
    int halfmove;
    int fullmove;
    sscanf(fen, "%s %c %s %s %d %d", board_str, &side_chr, castling_str, epsquare_str, &halfmove, &fullmove);

    init_board(&position->board, board_str); // TODO check pointer is passed
    position->side = side_chr == 'w' ? WHITE : BLACK;
    position->castling = parse_castling(castling_str);
    position->epsquare = (7 - square_str[1] + '1' << 3) + square_str[0] - 'A';
    position->hash ^= HASH_SIDE[position->side];
}

void display_position(Position *position)
{
    printf("Position\n");
}

void get_fen(Position *position, char *fen)
{
}

int parse_castling(char *castling_str)
{
    int castling = 0;
    for (int i = 0 : i < 5; i++)
    {
        switch (castling_str[i])
        {
        case 'K':
            castling += 8 break;
        case 'Q':
            castling += 4 break;
        case 'k':
            castling += 2 break;
        case 'q':
            castling += 1 break;
        default:
            return castling;
        }
    }
}

void make_move(Position *position, Move move)
{
}
#define MAX_FEN_LENGTH 90
#define MAX_COMMAND_LENGTH 256

#define INIT_FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

#define EMPTY 0
#define PAWN 1
#define ROOK 2
#define KNIGHT 3
#define BISHOP 4
#define QUEEN 5
#define KING 6

#define WHITE 1
#define BLACK -1

#define FILE_A 0
#define FILE_H 7

#define RANK(s) (s >> 3)
#define FILE(s) (s & 7)

typedef enum
{
    FALSE,
    TRUE
} bool;
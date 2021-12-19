#define MAX_COMMAND_LENGTH 256
#define MAX_FEN_LENGTH 90

#define INIT_FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

#define EMPTY 0

#define FILE(s) (s & 7)
#define RANK(s) (s >> 3)

#define FILE_A 0
#define FILE_H 7
#define RANK_8 7

// piece
#define PAWN 1
#define ROOK 2
#define KNIGHT 3
#define BISHOP 4
#define QUEEN 5
#define KING 6

// color
#define WHITE 1
#define BLACK -1

typedef enum {
    FALSE,
    TRUE
} bool;
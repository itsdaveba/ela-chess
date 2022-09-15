#define MAX_HPLY 512
#define MAX_DEPTH 8
#define MAX_GEN_MOVES 256
#define MAX_LAN_LENGTH 6
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

#define PAWN_MOVE 1
#define PAWN_DOUBLE_MOVE 2
#define PROMOTION 4
#define CAPTURE 8
#define CASTLE 16
#define EP_CAPTURE 32
#define ILLEGAL_MOVE 64
#define NO_MOVE 128

#define UP 8
#define DOWN -8
#define RIGHT 1
#define LEFT -1

#define UP_RIGHT 9
#define UP_LEFT 7
#define DOWN_RIGHT -7
#define DOWN_LEFT -9
#define DOUBLE_UP 16
#define DOUBLE_DOWN -16

#define A1 0
#define B1 1
#define C1 2
#define D1 3
#define E1 4
#define F1 5
#define G1 6
#define H1 7
#define A8 56
#define B8 57
#define C8 58
#define D8 59
#define E8 60
#define F8 61
#define G8 62
#define H8 63

#define FILE_A 0
#define FILE_H 7
#define RANK_2 1
#define RANK_7 6

#define FILE(s) (s & 7)
#define RANK(s) (s >> 3)
#define SQUARE(f, r) (((r - '1') << 3) + f - 'a')

typedef unsigned long long u64;
typedef enum
{
    FALSE,
    TRUE
} bool;
typedef struct
{
    int from;
    int to;
    int prom;
    int type;
} move_t;
typedef struct
{
    move_t move;
    int castling;
    int passant;
    int halfmove;
    int capture;
} hist_t;
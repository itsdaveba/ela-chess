#define MAX_HPLY 512
#define MAX_GEN_MOVES 256
#define MAX_BOOK_MOVES 32
#define MAX_PV_LENGTH 16
#define MAX_LAN_LENGTH 6
#define MAX_FEN_LENGTH 90
#define MAX_INPUT_LENGTH 256

#define MIN_SCORE -100000
#define MAX_SCORE 100000
#define MATE_THRESHOLD 90000
#define DRAW_SCORE 0

#define DEFAULT_TIME 500
#define DEFAULT_DEPTH 4

#define INIT_FEN "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#define BOOK_FILENAME "book.txt"

#define PAWN 0
#define ROOK 1
#define KNIGHT 2
#define BISHOP 3
#define QUEEN 4
#define KING 5
#define EMPTY 6

#define BLACK 0
#define WHITE 1

#define PAWN_MOVE 1
#define PAWN_DOUBLE_MOVE 2
#define PROMOTION 4
#define CAPTURE 8
#define CASTLE 16
#define EP_CAPTURE 32
#define ILLEGAL_MOVE 64
#define NO_MOVE -128

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
    char from;
    char to;
    char prom;
    char type;
} move_bytes;
typedef union
{
    int id;
    move_bytes bytes;
} move_t;
typedef struct
{
    int depth;
    move_t best[MAX_PV_LENGTH];
} line_t;
typedef struct
{
    move_t move;
    int castling;
    int passant;
    int halfmove;
    int capture;
    int hash;
} hist_t;
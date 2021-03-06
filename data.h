#include <setjmp.h>
#include <sys/time.h>

extern int ply;
extern int hply;
extern hist_t history[MAX_HPLY];

extern int n_moves[MAX_DEPTH + 32];
extern move_t move_list[MAX_DEPTH + 32][MAX_GEN_MOVES];

extern jmp_buf env;
extern struct timeval start, now;
extern int search_time;
extern int search_depth;
extern int nodes;

extern int piece[64];
extern int color[64];
extern int side;
extern int xside;
extern int castling;
extern int passant;
extern int halfmove;
extern int fullmove;

extern char piece_to_char[7];
extern char castling_char[4];
extern int board[64];
extern const int castling_rights[64];

extern const int slider[7];
extern const int n_directions[7];
extern const int direction[7][8];
extern const int mailbox[120];
extern const int mailbox64[64];

extern int piece_value[7];
extern int piece_table[7][64];
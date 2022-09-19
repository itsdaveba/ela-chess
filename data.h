#include <setjmp.h>

extern int piece[64];
extern int color[64];
extern int side;
extern int xside;
extern int castling;
extern int passant;
extern int halfmove;
extern int fullmove;

extern int ply;
extern int n_moves[MAX_DEPTH + MAX_QUIESCE];
extern move_t move_list[MAX_DEPTH + MAX_QUIESCE][MAX_GEN_MOVES];

extern int hply;
extern hist_t history[MAX_HPLY];

extern int nodes;
extern bool post;
extern jmp_buf env;
extern int search_time;
extern int search_depth;
extern struct timeval start, now;

extern const char piece_to_char[7];
extern const char castling_char[4];
extern const int board[64];
extern const int castling_rights[64];

extern const int slider[7];
extern const int n_directions[7];
extern const int direction[7][8];
extern const int mailbox[120];
extern const int mailbox64[64];

extern const int piece_value[7];
extern const int piece_table[7][64];
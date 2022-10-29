#include <stdio.h>
#include <setjmp.h>

extern FILE *book_file;
extern u64 nodes;
extern jmp_buf env;
extern int search_time;
extern int search_depth;
extern struct timeval start;
extern struct timeval now;

extern int ply;
extern int hply;
extern hist_t history[MAX_HPLY];
extern u64 hash_table[64][6][2];
extern transp_t transp_table[TRANSP_SIZE];

extern int piece[64];
extern int color[64];
extern int side;
extern int castling;
extern int passant;
extern int halfmove;
extern int fullmove;
extern u64 hash;

extern const char piece_char[7];
extern const char castling_char[4];
extern const int bigend_rank[64];
extern const int castling_rights[64];

extern const int slider[6];
extern const int n_directions[6];
extern const int direction[6][8];
extern const int mailbox[120];
extern const int mailbox64[64];

extern const int piece_value[6];
extern const int piece_table[6][64];
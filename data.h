extern int ply;
extern int hply;
extern hist_t history[MAX_PLIES];

extern int n_moves[MAX_DEPTH];
extern move_t move_list[MAX_DEPTH][MAX_GEN_MOVES];

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
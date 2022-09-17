// main.c
char *move_to_lan(move_t move);
move_t lan_to_move(char *lan);
bool print_result();

// board.c
bool set_board(char *fen);
char *get_fen();
void print_board();
void add_move(int from, int to, int type);
void gen_moves();
bool attack(int square, int side);
bool in_check(int side);
bool make_move(move_t move);
void take_back();
u64 perft(int depth);

// search.c
move_t search();
void shuffle_moves();
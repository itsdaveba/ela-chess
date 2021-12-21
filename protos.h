// main.c
int lan_to_move(char *lan);

// board.c
bool set_board(char *fen);
char *get_fen();
void print_board();
void add_move(int from, int to, int type);
void gen_moves();
bool attack(int square, int side);
bool in_check(int side);
bool make_move(int m);
void take_back();
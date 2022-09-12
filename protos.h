// board.c
bool set_board(char *fen);
char *get_fen();
void print_board();
void add_move(int from, int to, int type);
void gen_moves();
char *move_to_lan(move_t move);
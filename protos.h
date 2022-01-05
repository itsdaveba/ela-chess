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
u64 Perft(int depth);

// search.c
move_t search(bool post);
int negamax(int alpha, int beta, int depth, move_t *pline);
int quiesce(int alpha, int beta);
int get_time();
void swap(int m1, int m2);
void sort_move_list();

// eval.c
int evaluate();

// xboard.c
void xboard();
void print_result();
char *move_to_lan(move_t move);
move_t lan_to_move(char *lan);
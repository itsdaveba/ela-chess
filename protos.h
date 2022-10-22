// main.c
char *move_to_lan(move_t move);
move_t lan_to_move(char *lan);
bool print_result();

// board.c
bool set_board(char *fen);
char *get_fen();
void print_board();
void add_move(int from, int to, int type, int *n_moves, move_t *move_list);
int gen_moves(move_t *move_list, bool quiesce);
bool attack(int square, int side);
bool in_check(int side);
bool make_move(move_t move);
void take_back();
u64 perft(int depth);

// search.c
move_t search(bool post, bool book);
int negamax(int alpha, int beta, int depth, line_t *pline);
int quiesce(int alpha, int beta, line_t *pline);
void shuffle_moves(int n_moves, move_t *move_list);

// eval.c
int evaluate();

// book.c
bool open_book();
void close_book();
move_t book_move();
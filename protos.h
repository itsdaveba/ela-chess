// main.c
char *move_to_lan(move_t move);
move_t lan_to_move(char *lan);
bool print_result();

// board.c
bool set_board(char *fen);
char *get_fen();
void print_board();
void add_move(int from, int to, int type, int *n_moves, gen_t *move_list);
int gen_moves(gen_t *move_list, bool quiesce);
move_t gen_capture(int from, int to, int prom);
int attacker(int square, int side, int skip);
bool in_check(int side);
bool make_move(move_t move);
void take_back();
int repetition();
u64 perft(int depth);

// search.c
move_t search(bool post, bool book);
int negamax(int alpha, int beta, int depth);
int quiesce(int alpha, int beta);
void print_pv();
int time_diff(struct timeval start, struct timeval stop);
void check_time();
void score_move(move_t move, int score, int n_moves, gen_t *move_list);
void swap_moves(gen_t *move_x, gen_t *move_y);
void shuffle_moves(int n_moves, gen_t *move_list);
void sort_move(int m, int n_moves, gen_t *move_list);

// eval.c
int evaluate();
int see(int square, int side);
int see_capture(move_t move);

// book.c
bool open_book();
void close_book();
move_t book_move();

// hash.c
u64 rand_hash();
void init_hash();
void set_hash();
void store_hash(int score, int depth, int node_type, move_t best_move);
bool probe_hash(int alpha, int beta, int depth, int *score, move_t *best_move);
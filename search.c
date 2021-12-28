#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>
#include <sys/time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int search(bool post) {

    int val;
    int max;
    int n_max;
    int score;
    int best_move;
    move_t tmp_move;
    
    int max_args[MAX_GEN_MOVES];

    nodes = 0;

    gettimeofday(&start, NULL);

    val = setjmp(env);
    if(val) {
        while(ply) {
            take_back();
        }
        return 0;
    }

    if(search_depth == 0) {
        n_max = 0;
        for(int m = 0; m < n_moves[ply]; m++) {
            if(make_move(m)) {
                max_args[n_max++] = m;
                take_back();
            }
        }
        if(n_max) {
            return max_args[rand() % n_max];
        }
        return -1;
    }

    for(int depth = 1; depth <= search_depth; depth++) {
        max = INT_MIN + 1;
        for(int m = 0; m < n_moves[ply]; m++) {
            if(make_move(m)) {
                score = -negamax(INT_MIN + 1, INT_MAX, depth - 1);
                take_back();
                if(score == INT_MAX) {
                    if(post) {
                        printf("%d %d %d %d %s\n", depth, 100001 - depth, get_time(), nodes, move_to_lan(m));
                    }
                    return m;
                }
                if(score > max) {
                    n_max = 0;
                    max = score;
                }
                if(score == max) {
                    max_args[n_max++] = m;
                }
            }
        }
        if(max == INT_MIN + 1) {
            best_move = max_args[rand() % n_max];
            if(post) {
                printf("%d %d %d %d %s\n", depth, -100001 + depth, get_time(), nodes, move_to_lan(best_move));
            }
            return best_move;
        }
        best_move = max_args[rand() % n_max];
        tmp_move = move_list[0][best_move];
        move_list[0][best_move] = move_list[0][0];
        move_list[0][0] = tmp_move;
        if(post) {
            printf("%d %d %d %d %s\n", depth, max, get_time(), nodes, move_to_lan(0));
        }
    }

    return 0;
}

int negamax(int alpha, int beta, int depth) {

    if(depth == 0) {
        return quiesce(alpha, beta);
    }

    int score;

    gen_moves();
    for(int m = 0; m < n_moves[ply]; m++) {
        if(make_move(m)) {
            score = -negamax(-beta, -alpha, depth - 1);
            take_back();
            if(score >= beta) {
                return beta;
            }
            if(score > alpha) {
                alpha = score;
            }
        }
    }

    return alpha;
}

int quiesce(int alpha, int beta) {

    nodes++;
    if(nodes % 32768 == 0) {
        if(get_time() >= search_time) {
            longjmp(env, 1);
        }
    }

    int score;
    int stand_pat = evaluate();

    if(stand_pat >= beta) {
        return beta;
    }
    if(alpha < stand_pat) {
        alpha = stand_pat;
    }

    gen_moves();
    for(int m = 0; m < n_moves[ply]; m++) {
        if((move_list[ply][m].type & CAPTURE) && make_move(m)) {
            score = -quiesce(-beta, -alpha);
            take_back();
            if(score >= beta) {
                return beta;
            }
            if(score > alpha) {
                alpha = score;
            }
        }
    }

    return alpha;
}

int get_time() {
    gettimeofday(&now, NULL);
    return (now.tv_sec - start.tv_sec) * 100 + (now.tv_usec - start.tv_usec) / 10000;
}
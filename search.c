#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include <sys/time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

move_t search(bool post) {

    int val;
    int max;
    int n_max;
    int score;
    int best_move;
    move_t move;
    move_t tmp_move;
    
    int max_args[MAX_GEN_MOVES];
    move_t pv[MAX_DEPTH + 32];

    nodes = 0;

    gettimeofday(&start, NULL);

    val = setjmp(env);
    if(val) {
        while(ply) {
            take_back();
        }
        return pv[0];
    }

    if(search_depth == 0) {
        n_max = 0;
        for(int m = 0; m < n_moves[ply]; m++) {
            if(make_move(move_list[ply][m])) {
                max_args[n_max++] = m;
                take_back();
            }
        }
        if(n_max) {
            return move_list[ply][max_args[rand() % n_max]];
        }
        move.type = NO_MOVE;
        return move;
    }

    move_t line[MAX_DEPTH];

    for(int depth = 1; depth <= search_depth; depth++) {
        max = -99999;
        for(int m = 0; m < n_moves[0]; m++) {
            if(make_move(move_list[0][m])) {
                score = -negamax(-99999, 99999, depth - 1, line);
                move_list[0][m].score = score;
                take_back();
                if(move_list[0][m].score > max) {
                    n_max = 0;
                    max = move_list[0][m].score;
                }
                if(move_list[0][m].score == max) {
                    pv[0] = move_list[0][m];
                    memcpy(pv + 1, line, (depth - 1) * sizeof(move_t));
                    if(post) {
                        printf("%d %d %d %d", depth, max, get_time(), nodes);
                        for(int d = 0; d < depth; d++) {
                            printf(" %s", move_to_lan(pv[d]));
                        }
                        printf("\n");
                    }
                    if(max == 99999) {
                        return move_list[0][m];
                    }
                    max_args[n_max++] = m;
                }
            }
            else if(move_list[0][m].score != INT_MIN){
                move_list[0][m].score = INT_MIN;
            }
        }
        if(max == -99999) {
            return move_list[0][0];
        }
        sort_move_list();
        swap(0, rand() % n_max);
    }

    return move_list[0][0];
}

int negamax(int alpha, int beta, int depth, move_t *pline) {

    if(depth == 0) {
        return quiesce(alpha, beta);
    }

    int score;
    move_t line[MAX_DEPTH];

    gen_moves();
    for(int m = 0; m < n_moves[ply]; m++) {
        if(make_move(move_list[ply][m])) {
            score = -negamax(-beta, -alpha, depth - 1, line);
            take_back();
            if(score >= beta) {
                return beta;
            }
            if(score > alpha) {
                alpha = score;
                *pline = move_list[ply][m];
                memcpy(pline + 1, line, (depth - 1) * sizeof(move_t));
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
        if((move_list[ply][m].type & CAPTURE) && make_move(move_list[ply][m])) {
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

void swap(int m1, int m2) {
    move_t tmp;
    tmp = move_list[0][m1];
    move_list[0][m1] = move_list[0][m2];
    move_list[0][m2] = tmp;
}

void sort_move_list() {
    bool swaped = TRUE;
    while(swaped) {
        swaped = FALSE;
        for(int m = n_moves[0] - 1; m > 0; m--) {
            if(move_list[0][m-1].score < move_list[0][m].score) {
                swap(m-1, m);
                swaped = TRUE;
            }
        }
    }
}
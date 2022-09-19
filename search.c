#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
#include <sys/time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

move_t search() {

    int alpha;
    int beta;
    int score;
    move_t pline[MAX_DEPTH];
    move_t line[MAX_DEPTH];

    nodes = 0;

    shuffle_moves();
    gettimeofday(&start, NULL);

    if(setjmp(env)) {
        while(ply) {
            take_back();
        }
        return pline[0];
    }

    if(search_depth == 0) {
        for(int m = 0; m < n_moves[0]; m++) {
            if(make_move(move_list[0][m])) {
                take_back();
                return move_list[0][m];
            }
        }
        // return null move
    }

    for(int depth = 1; depth <= search_depth; depth++) {
        alpha = MIN_SCORE;
        beta = MAX_SCORE;
        for(int m = 0; m < n_moves[0]; m++) {
            if(make_move(move_list[0][m])) {
                score = -negamax(-beta, -alpha, depth - 1, line);
                take_back();
                if(score >= beta) {
                    *pline = move_list[0][m];
                    memcpy(pline + 1, line, (depth - 1) * sizeof(move_t));
                    if(post) {
                        gettimeofday(&now, NULL);
                        printf("%d %d %d %d", depth, score - depth, (now.tv_sec - start.tv_sec) * 100 + (now.tv_usec - start.tv_usec) / 10000, nodes);
                        for(int d = 0; d < depth - 1; d++) {
                            printf(" %s", move_to_lan(pline[d]));
                        }
                        printf("\n");
                    }
                    return pline[0];
                }
                if(score > alpha) {
                    alpha = score;
                    *pline = move_list[0][m];
                    memcpy(pline + 1, line, (depth - 1) * sizeof(move_t));
                    if(post) {
                        gettimeofday(&now, NULL);
                        printf("%d %d %d %d", depth, alpha, (now.tv_sec - start.tv_sec) * 100 + (now.tv_usec - start.tv_usec) / 10000, nodes);
                        for(int d = 0; d < depth; d++) {
                            printf(" %s", move_to_lan(pline[d]));
                        }
                        printf("\n");
                    }
                }
            }
        }
    }

    return pline[0];
}

int negamax(int alpha, int beta, int depth, move_t *pline) {

    if(depth == 0) {
        return quiesce(alpha, beta);
    }

    int score;
    move_t line[MAX_DEPTH];

    gen_moves(); // shuffle

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
        gettimeofday(&now, NULL);
        if((now.tv_sec - start.tv_sec) * 100 + (now.tv_usec - start.tv_usec) / 10000 >= search_time) {
            longjmp(env, TRUE);
        }
    }

    int score;
    int stand_pat = evaluate();

    if(stand_pat >= beta) {
        return beta;
    }
    if(stand_pat > alpha) {
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

void shuffle_moves() {

    int n;
    move_t tmp;

    for(int m = n_moves[ply] - 1; m > 0; m--) {
        n = rand() % (m + 1);
        tmp = move_list[ply][m];
        move_list[ply][m] = move_list[ply][n];
        move_list[ply][n] = tmp;
    }
}
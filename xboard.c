#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

void xboard() {

    int m;
    char *lan;
    char line[MAX_COMMAND_LENGTH];
    char command[MAX_COMMAND_LENGTH];
    int computer_side = EMPTY;

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    printf("\n");

    while(TRUE) {

        if(side == computer_side) {
            m = search();
            if(m == -1) {
                computer_side = EMPTY;
                continue;
            }
            lan = move_to_lan(m);
            printf("move %s\n", lan);
            make_move(m);
            ply = 0;
            gen_moves();
            print_result();
            continue;
        }

        fgets(line, MAX_FEN_LENGTH, stdin);
        sscanf(line, "%s", command);

        if(!strcmp(command, "new")) {
            computer_side = BLACK;
            set_board(INIT_FEN);
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "quit")) {
            break;
        }
        if(!strcmp(command, "go")) {
            computer_side = side;
            continue;
        }
        
        m = lan_to_move(command);
        if(m == -1) {
            printf("Error (uknown command): %s\n", command);
            continue;
        }
        if(m == -2 || !make_move(m)) {
            printf("Illegal move: %s\n", command);
            continue;
        }
        ply = 0;
        gen_moves();
        print_result();
    }
}

void print_result() {

    int m;

    for(m = 0; m < n_moves[ply]; m++) {
        if(make_move(m)) {
            take_back();
            break;
        }
    }

    if(m == n_moves[ply]) {
        if(in_check(side)) {
            if(side == WHITE) {
                printf("0-1 {Black mates}\n");
            }
            else {
                printf("1-0 {White mates}\n");
            }
        }
        else {
            printf("1/2-1/2 {Stalemate}\n");
        }
    }
    else if(halfmove >= 100) {
        printf("1/2-1/2 {Draw by fifty move rule}\n");
    }
    
}

char *move_to_lan(int m) {

    static char lan[MAX_LAN_LENGTH];

    move_t move = move_list[ply][m];

    lan[0] = FILE(move.from) + 'a';
    lan[1] = RANK(move.from) + '1';
    lan[2] = FILE(move.to) + 'a';
    lan[3] = RANK(move.to) + '1';

    if(move.type & PROMOTION) {
        if(color[move.from] == WHITE) {
            lan[4] = piece_to_char[move.prom];
        }
        else {
            lan[4] = piece_to_char[move.prom] | ' ';
        }            
    }
    else if(lan[4] != '\0') {
        lan[4] = '\0';
    }

    return lan;
}

int lan_to_move(char *lan) {

    if(lan[0] < 'a' || lan[0] > 'h' ||
       lan[1] < '1' || lan[1] > '8' ||
       lan[2] < 'a' || lan[2] > 'h' ||
       lan[3] < '1' || lan[3] > '8') {
        return -1;
    } 

    int from = ((lan[1] - '1') << 3) + lan[0] - 'a';
    int to = ((lan[3] - '1') << 3) + lan[2] - 'a';
    int prom;

    switch(lan[4] | ' ') {
        case ' ': prom = EMPTY; break;
        case 'r': prom = ROOK; break;
        case 'n': prom = KNIGHT; break;
        case 'b': prom = BISHOP; break;
        case 'q': prom = QUEEN; break;
        default: return -1;
    }

    for(int m = 0; m < n_moves[ply]; m++) {
        if(move_list[ply][m].from == from && move_list[ply][m].to == to && move_list[ply][m].prom == prom) {
            return m;
        }
    }
    return -2;
    
}
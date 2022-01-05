#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

void xboard() {

    char *lan;
    move_t move;
    char line[MAX_COMMAND_LENGTH];
    char command[MAX_COMMAND_LENGTH];
    int computer_side = EMPTY;
    bool post = FALSE;

    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    printf("\n");

    while(TRUE) {

        if(side == computer_side) {
            move = search(post);
            if(move.type == NO_MOVE) {
                computer_side = EMPTY;
                continue;
            }
            lan = move_to_lan(move);
            printf("move %s\n", lan);
            make_move(move);
            ply = 0;
            gen_moves();
            print_result();
            continue;
        }

        fgets(line, MAX_FEN_LENGTH, stdin);
        sscanf(line, "%s", command);

        if(!strcmp(command, "new")) {
            computer_side = BLACK;
            search_time = DEFAULT_TIME;
            search_depth = MAX_DEPTH;
            set_board(INIT_FEN);
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "quit")) {
            break;
        }
        if(!strcmp(command, "random")) {
            continue;
        }
        if(!strcmp(command, "force")) {
            computer_side = EMPTY;
            continue;
        }
        if(!strcmp(command, "go")) {
            computer_side = side;
            continue;
        }
        if(!strcmp(command, "white")) {
            computer_side = BLACK;
            side = WHITE;
            xside = BLACK;
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "black")) {
            computer_side = WHITE;
            side = BLACK;
            xside = WHITE;
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "level")) {
            continue;
        }
        if(!strcmp(command, "st")) {
            sscanf(line, "st %d", &search_time);
            search_depth = MAX_DEPTH;
            search_time *= 100;
            if(search_time > MAX_TIME) {
                search_time = MAX_TIME;
            }
            continue;
        }
        if(!strcmp(command, "sd")) {
            sscanf(line, "sd %d", &search_depth);
            search_time = MAX_TIME;
            if(search_depth > MAX_DEPTH) {
                search_depth = MAX_DEPTH;
            }
            continue;
        }
        if(!strcmp(command, "time")) {
            continue;
        }
        if(!strcmp(command, "otim")) {
            continue;
        }
        if(!strcmp(command, "?")) {
            continue;
        }
        if(!strcmp(command, "draw")) {
            continue;
        }
        if(!strcmp(command, "result")) {
            continue;
        }
        if(!strcmp(command, "edit")) {
            side = WHITE;
            while(TRUE) {
                scanf("%s", command);
                if(!strcmp(command, "#")) {
                    set_board(CLEAR_FEN);
                    continue;
                }
                if(!strcmp(command, "c")) {
                    side = -side;
                    continue;
                }
                if(!strcmp(command, ".")) {
                    break;
                }
                switch(command[0]) {
                    case 'P': piece[((command[2] - '1') << 3) + command[1] - 'a'] = PAWN; break;
                    case 'R': piece[((command[2] - '1') << 3) + command[1] - 'a'] = ROOK; break;
                    case 'N': piece[((command[2] - '1') << 3) + command[1] - 'a'] = KNIGHT; break;
                    case 'B': piece[((command[2] - '1') << 3) + command[1] - 'a'] = BISHOP; break;
                    case 'Q': piece[((command[2] - '1') << 3) + command[1] - 'a'] = QUEEN; break;
                    case 'K': piece[((command[2] - '1') << 3) + command[1] - 'a'] = KING; break;
                }
                color[((command[2] - '1') << 3) + command[1] - 'a'] = side;
            }
            fflush(stdin);
            side = -xside;
            castling = 0;
            if(piece[E1] == KING && color[E1] == WHITE) {
                if(piece[H1] == ROOK && color[H1] == WHITE) {
                    castling |= 0b1000;
                }
                if(piece[A1] == ROOK && color[A1] == WHITE) {
                    castling |= 0b0100;
                }
            }
            if(piece[E8] == KING && color[E8] == BLACK) {
                if(piece[H8] == ROOK && color[H8] == BLACK) {
                    castling |= 0b0010;
                }
                if(piece[A8] == ROOK && color[A8] == BLACK) {
                    castling |= 0b0001;
                }
            }
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "hint")) {
            continue;
        }
        if(!strcmp(command, "bk")) {
            continue;
        }
        if(!strcmp(command, "undo")) {
            if(hply == 0) {
                continue;
            }
            take_back();
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "remove")) {
            if(hply == 0) {
                continue;
            }
            take_back();
            take_back();
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "hard")) {
            continue;
        }
        if(!strcmp(command, "easy")) {
            continue;
        }
        if(!strcmp(command, "post")) {
            post = TRUE;
            continue;
        }
        if(!strcmp(command, "nopost")) {
            post = FALSE;
            continue;
        }
        if(!strcmp(command, "analyze")) {
            // TODO
            continue;
        }
        if(!strcmp(command, "name")) {
            continue;
        }
        if(!strcmp(command, "rating")) {
            continue;
        }
        if(!strcmp(command, "computer")) {
            continue;
        }
        
        move = lan_to_move(command);
        if(move.type == NO_MOVE) {
            printf("Error (unknown command): %s\n", command);
            continue;
        }
        if(move.type == ILLEGAL_MOVE || !make_move(move)) {
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
        if(make_move(move_list[ply][m])) {
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

char *move_to_lan(move_t move) {

    static char lan[MAX_LAN_LENGTH];

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

move_t lan_to_move(char *lan) {

    move_t move;

    if(lan[0] < 'a' || lan[0] > 'h' ||
       lan[1] < '1' || lan[1] > '8' ||
       lan[2] < 'a' || lan[2] > 'h' ||
       lan[3] < '1' || lan[3] > '8') {
        move.type = NO_MOVE;
        return move;
    } 

    move.from = ((lan[1] - '1') << 3) + lan[0] - 'a';
    move.to = ((lan[3] - '1') << 3) + lan[2] - 'a';

    switch(lan[4] | ' ') {
        case ' ': move.prom = EMPTY; break;
        case 'r': move.prom = ROOK; break;
        case 'n': move.prom = KNIGHT; break;
        case 'b': move.prom = BISHOP; break;
        case 'q': move.prom = QUEEN; break;
        default: {
            move.type = NO_MOVE;
            return move;
        }
    }

    for(int m = 0; m < n_moves[ply]; m++) {
        if(move_list[ply][m].from == move.from && move_list[ply][m].to == move.to && move_list[ply][m].prom == move.prom) {
            move.type = move_list[ply][m].type;
            return move;
        }
    }
    move.type = ILLEGAL_MOVE;
    return move;

}
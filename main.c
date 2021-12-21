#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int main() {

    printf("Ela Chess Program\n\n");

    int m;
    char *fen;
    char command[MAX_COMMAND_LENGTH];

    set_board(INIT_FEN);
    fen = get_fen();
    
    while(TRUE) {

        printf("ela> ");
        if(scanf("%s", command) == EOF) {
            break;
        }

        if(!strcmp(command, "new")) {
            set_board(INIT_FEN);
        }
        else if(!strcmp(command, "fen")) {
            getchar();
            fgets(fen, MAX_FEN_LENGTH, stdin);
            fen[strcspn(fen, "\n")] = '\0';
            if(!set_board(fen)) {
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
        }
        else if(!strcmp(command, "d")) {
            print_board();
        }
        else if(!strcmp(command, "exit")) {
            break;
        }
        else {
            gen_moves();
            m = lan_to_move(command);
            if(m == -1) {
                printf("Error: uknown command\n");
            }
            else if(m == -2 || !make_move(m)) {
                printf("Illegal move\n");
            }
        }

    }

    return 0;
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

    for(int m = 0; m < n_moves; m++) {
        if(move_list[m].from == from && move_list[m].to == to && move_list[m].prom == prom) {
            return m;
        }
    }
    return -2;
    
}
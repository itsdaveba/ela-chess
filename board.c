#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

// set board state from FEN
bool set_board(char *fen) {
    
    char copy[MAX_FEN_LENGTH];
    strcpy(copy, fen);

    char *brd = strtok(copy, " ");

    char *sd = strtok(NULL, " ");
    if(sd == NULL || !strcmp(sd, "w")) {
        side = WHITE;
        xside = BLACK;
    }
    else if(!strcmp(sd, "b")) {
        side = BLACK;
        xside = WHITE;
    }
    else {
        return FALSE;
    }

    char *castl = strtok(NULL, " ");
    castling = 0;
    if(castl != NULL && strcmp(castl, "-")) {
        for(int i = 0; i < strlen(castl); i++) {
            if(castl[i + 1] != '\0' && castl[i] >= castl[i + 1]) {
                return FALSE;
            }
            switch(castl[i]) {
                case 'K': castling |= 0b1000; break;
                case 'Q': castling |= 0b0100; break;
                case 'k': castling |= 0b0010; break;
                case 'q': castling |= 0b0001; break;
                default: return FALSE;
            }
        }
    }

    char *pass = strtok(NULL, " ");
    if(pass == NULL || !strcmp(pass, "-")) {
        passant = -1;
    }
    else if(pass[0] < 'a' || pass[0] > 'h' || (pass[1] != '3' && pass[1] != '6') || pass[2] != '\0') {
        return FALSE;
    }
    else {
        passant = ((pass[1] - '1') << 3) + pass[0] - 'a';
    }

    char *hf = strtok(NULL, "");
    if(hf == NULL) {
        halfmove = 0;
        fullmove = 1;
    }
    else if(sscanf(hf, "%d %d", &halfmove, &fullmove) < 2) {
        return FALSE;
    }
    else if(halfmove < 0 || fullmove < 1) {
        return FALSE;
    }

    char *row = strtok(brd, "/");
    if(row == NULL) {
        return FALSE;
    }
    int s = 0;
    while(row != NULL) {
        if(strlen(row) > 8) {
            return FALSE;
        }
        for(int c = 0; c < strlen(row); c++) {
            if(row[c] & '@') {
                if(row[c] & ' ') {
                    row[c] ^= ' ';
                    color[board[s]] = BLACK;
                }
                else {
                    color[board[s]] = WHITE;
                }
                switch(row[c]) {
                    case 'P': piece[board[s++]] = PAWN; break;
                    case 'R': piece[board[s++]] = ROOK; break;
                    case 'N': piece[board[s++]] = KNIGHT; break;
                    case 'B': piece[board[s++]] = BISHOP; break;
                    case 'Q': piece[board[s++]] = QUEEN; break;
                    case 'K': piece[board[s++]] = KING; break;
                    default: return FALSE;
                }
            }
            else if(row[c] < '1' || row[c] > '8') {
                return FALSE;
            }
            else {
                for(int i = 0; i < row[c] - '0'; i++) {
                    piece[board[s]] = EMPTY;
                    color[board[s++]] = EMPTY;
                }
            }
        }
        if(FILE(s) != FILE_A) {
            return FALSE;
        }
        row = strtok(NULL, "/");
    }
    if(s != 64) {
        return FALSE;
    }

    return TRUE;
}

// get FEN from board state
char *get_fen() {

    static char fen[MAX_FEN_LENGTH];

    int ctr;
    int c = 0;

    for(int s = 0; s < 64; s++) {
        if(piece[board[s]] == EMPTY) {
            for(ctr = 1; FILE(board[s]) != FILE_H && piece[board[s + 1]] == EMPTY; s++) {
                ctr++;
            }
            fen[c++] = ctr + '0';
        }
        else {
            if(color[board[s]] == WHITE) {
                fen[c++] = piece_to_char[piece[board[s]]];
            }
            else {
                fen[c++] = piece_to_char[piece[board[s]]] | ' ';
            }
        }
        if(FILE(board[s]) == FILE_H && s != 63) {
            fen[c++] = '/';
        }
    }
    fen[c++] = ' ';

    if(side == WHITE) {
        fen[c++] = 'w';
    }
    else {
        fen[c++] = 'b';
    }
    fen[c++] = ' ';

    if(castling != 0) {
        int bit = 0b1000;
        for(int i = 0; i < 4; i++) {
            if(castling & bit) {
                fen[c++] = castling_char[i];
            }
            bit >>= 1;
        }
    }
    else {
        fen[c++] = '-';
    }
    fen[c++] = ' ';

    if(passant != -1) {
        fen[c++] = FILE(passant) + 'a';
        fen[c++] = RANK(passant) + '1';
    }
    else {
        fen[c++] = '-';
    }
    fen[c++] = ' ';

    sprintf(fen + c, "%d %d", halfmove, fullmove);
    
    return fen;
}

// print FEN and ASCII board
void print_board() {
    char *fen = get_fen();
    printf("\n%s\n", fen);
    printf("\n  A B C D E F G H");
    for(int s = 0; s < 64; s++) {
        if(FILE(board[s]) == FILE_A) {
            printf("\n%d", RANK(board[s]) + 1);
        }
        if(color[board[s]] == WHITE) {
            printf(" %c", piece_to_char[piece[board[s]]]);
        }
        else {
            printf(" %c", piece_to_char[piece[board[s]]] | ' ');
        }
    }
    printf("\n\n");
}

// add move to move_list
void add_move(int from, int to, int type) {
    move_t *move_p = &move_list[ply][n_moves[ply]];
    if(type & PROMOTION) {
        for(int prom = ROOK; prom <= QUEEN; prom++) {
            n_moves[ply]++;
            move_p->from = from;
            move_p->to = to;
            move_p->prom = prom;
            move_p++->type = type;
        }
    }
    else {
        n_moves[ply]++;
        move_p->from = from;
        move_p->to = to;
        move_p->prom = EMPTY;
        move_p->type = type;
    }
}

// generate pseudo-legal moves
void gen_moves() {

    int type;

    n_moves[ply] = 0;

    for(int s = 0; s < 64; s++) {
        if(color[s] == side) {
            if(piece[s] == PAWN) {
                type = PAWN_MOVE;
                if(color[s] == WHITE) {
                    if(piece[s + UP] == EMPTY) {
                        if(RANK(s) == RANK_7) {
                            add_move(s, s + UP, type | PROMOTION);
                        }
                        else {
                            add_move(s, s + UP, type);
                        }
                        if(RANK(s) == RANK_2 && piece[s + DOUBLE_UP] == EMPTY) {
                            add_move(s, s + DOUBLE_UP, type | PAWN_DOUBLE_MOVE);
                        }
                    }
                    type |= CAPTURE;
                    if(FILE(s) != FILE_A) {
                        if(color[s + UP_LEFT] == xside) {
                            if(RANK(s) == RANK_7) {
                                add_move(s, s + UP_LEFT, type | PROMOTION);
                            }
                            else {
                                add_move(s, s + UP_LEFT, type);
                            }
                        }
                    }
                    if(FILE(s) != FILE_H) {
                        if(color[s + UP_RIGHT] == xside) {
                            if(RANK(s) == RANK_7) {
                                add_move(s, s + UP_RIGHT, type | PROMOTION);
                            }
                            else {
                                add_move(s, s + UP_RIGHT, type);
                            }
                        }
                    }
                }
                else {
                    if(piece[s + DOWN] == EMPTY) {
                        if(RANK(s) == RANK_2) {
                            add_move(s, s + DOWN, type | PROMOTION);
                        }
                        else {
                            add_move(s, s + DOWN, type);
                        }
                        if(RANK(s) == RANK_7 && piece[s + DOUBLE_DOWN] == EMPTY) {
                            add_move(s, s + DOUBLE_DOWN, type | PAWN_DOUBLE_MOVE);
                        }
                    }
                    type |= CAPTURE;
                    if(FILE(s) != FILE_A) {
                        if(color[s + DOWN_LEFT] == xside) {
                            if(RANK(s) == RANK_2) {
                                add_move(s, s + DOWN_LEFT, type | PROMOTION);
                            }
                            else {
                                add_move(s, s + DOWN_LEFT, type);
                            }
                        }
                    }
                    if(FILE(s) != FILE_H) {
                        if(color[s + DOWN_RIGHT] == xside) {
                            if(RANK(s) == RANK_2) {
                                add_move(s, s + DOWN_RIGHT, type | PROMOTION);
                            }
                            else {
                                add_move(s, s + DOWN_RIGHT, type);
                            }
                        }
                    }
                }
            }
            else {
                for(int d = 0; d < n_directions[piece[s]]; d++) {
                    for(int n = s;;) {
                        n = mailbox[mailbox64[n] + direction[piece[s]][d]];
                        if(n == -1) {
                            break;
                        }
                        if(color[n] != EMPTY) {
                            if(color[n] == xside) {
                                add_move(s, n, CAPTURE);
                            }
                            break;
                        }
                        add_move(s, n, 0);
                        if(!slider[piece[s]]) {
                            break;
                        }
                    }
                }
            }
        }
    }

    if(castling != 0) {
        if(side == WHITE) {
            if(!attack(E1, BLACK)) {
                if(castling & 0b1000) {
                    if(piece[F1] == EMPTY && piece[G1] == EMPTY) {
                        if(!attack(F1, BLACK)) {
                            add_move(E1, G1, CASTLE);
                        }
                    }
                }
                if(castling & 0b0100) {
                    if(piece[D1] == EMPTY && piece[C1] == EMPTY && piece[B1] == EMPTY) {
                        if(!attack(D1, BLACK)) {
                            add_move(E1, C1, CASTLE);
                        }
                    }
                }
            }
        }
        else {
            if(!attack(E8, WHITE)) {
                if(castling & 0b0010) {
                    if(piece[F8] == EMPTY && piece[G8] == EMPTY) {
                        if(!attack(F8, WHITE)) {
                            add_move(E8, G8, CASTLE);
                        }
                    }
                }
                if(castling & 0b0001) {
                    if(piece[D8] == EMPTY && piece[C8] == EMPTY && piece[B8] == EMPTY) {
                        if(!attack(D8, WHITE)) {
                            add_move(E8, C8, CASTLE);
                        }
                    }
                }
            }
        }
    }

    if(passant != -1) {
        type = PAWN_MOVE | CAPTURE | EP_CAPTURE;
        if(side == WHITE) {
            if(FILE(passant) != FILE_A) {
                if(piece[passant + DOWN_LEFT] == PAWN && color[passant + DOWN_LEFT] == WHITE) {
                    add_move(passant + DOWN_LEFT, passant, type);
                }
            }
            if(FILE(passant) != FILE_H) {
                if(piece[passant + DOWN_RIGHT] == PAWN && color[passant + DOWN_RIGHT] == WHITE) {
                    add_move(passant + DOWN_RIGHT, passant, type);
                }
            }
        }
        else {
            if(FILE(passant) != FILE_A) {
                if(piece[passant + UP_LEFT] == PAWN && color[passant + UP_LEFT] == BLACK) {
                    add_move(passant + UP_LEFT, passant, type);
                }
            }
            if(FILE(passant) != FILE_H) {
                if(piece[passant + UP_RIGHT] == PAWN && color[passant + UP_RIGHT] == BLACK) {
                    add_move(passant + UP_RIGHT, passant, type);
                }
            }
        }
    }

}

// is square attacked by side
bool attack(int square, int side) {
    for(int s = 0; s < 64; s++) {
        if(color[s] == side) {
            if(piece[s] == PAWN) {
                if(color[s] == WHITE) {
                    if(FILE(s) != FILE_A) {
                        if(square == s + UP_LEFT) {
                            return TRUE;
                        }
                    }
                    if(FILE(s) != FILE_H) {
                        if(square == s + UP_RIGHT) {
                            return TRUE;
                        }
                    }
                }
                else {
                    if(FILE(s) != FILE_A) {
                        if(square == s + DOWN_LEFT) {
                            return TRUE;
                        }
                    }
                    if(FILE(s) != FILE_H) {
                        if(square == s + DOWN_RIGHT) {
                            return TRUE;
                        }
                    }
                }
            }
            else {
                for(int d = 0; d < n_directions[piece[s]]; d++) {
                    for(int n = s;;) {
                        n = mailbox[mailbox64[n] + direction[piece[s]][d]];
                        if(n == -1) {
                            break;
                        }
                        if(square == n) {
                            return TRUE;
                        }
                        if(color[n] != EMPTY) {
                            break;
                        }
                        if(!slider[piece[s]]) {
                            break;
                        }
                    }
                }
            }
        }
    }
    return FALSE;
}

// is king's side in check
bool in_check(int side) {
    for(int s = 0; s < 64; s++) {
        if(piece[s] == KING && color[s] == side) {
            if(side == WHITE) {
                return attack(s, BLACK);
            }
            else {
                return attack(s, WHITE);
            }
        }
    }
    return FALSE;
}

// make move if it's legal
bool make_move(move_t move) {

    ply++;

    history[hply].move = move;
    history[hply].castling = castling;
    history[hply].passant = passant;
    history[hply].halfmove = halfmove;
    history[hply++].capture = piece[move.to];

    if(move.type & PROMOTION) {
        piece[move.to] = move.prom;
    }
    else {
        piece[move.to] = piece[move.from];
    }
    color[move.to] = side;
    piece[move.from] = EMPTY;
    color[move.from] = EMPTY;

    if(castling != 0) {
        castling &= castling_rights[move.from] & castling_rights[move.to];
    }

    if(move.type & PAWN_DOUBLE_MOVE) {
        if(side == WHITE) {
            passant = move.to + DOWN;
        }
        else {
            passant = move.to + UP;
        }
    }
    else if(passant != -1) {
        passant = -1;
    }

    if(move.type & (PAWN_MOVE | CAPTURE)) {
        halfmove = 0;
    }
    else {
        halfmove++;
    }

    if(side == BLACK) {
        fullmove++;
    }

    if(move.type & CASTLE) {
        if(move.to > move.from) {
            if(side == WHITE) {
                piece[F1] = piece[H1];
                color[F1] = WHITE;
                piece[H1] = EMPTY;
                color[H1] = EMPTY;
            }
            else {
                piece[F8] = piece[H8];
                color[F8] = BLACK;
                piece[H8] = EMPTY;
                color[H8] = EMPTY;
            }
        }
        else {
            if(side == WHITE) {
                piece[D1] = piece[A1];
                color[D1] = WHITE;
                piece[A1] = EMPTY;
                color[A1] = EMPTY;
            }
            else {
                piece[D8] = piece[A8];
                color[D8] = BLACK;
                piece[A8] = EMPTY;
                color[A8] = EMPTY;
            }
        }
    }
    
    if(move.type & EP_CAPTURE) {
        if(side == WHITE) {
            piece[move.to + DOWN] = EMPTY;
            color[move.to + DOWN] = EMPTY;
        }
        else {
            piece[move.to + UP] = EMPTY;
            color[move.to + UP] = EMPTY;
        }
    }

    side = xside;
    xside = -side;

    if(in_check(xside)) {
        take_back();
        return FALSE;
    }

    return TRUE;
}

// take back last move
void take_back() {

    hist_t hist = history[--hply];
    --ply;

    side = xside;
    xside = -side;

    castling = hist.castling;
    passant = hist.passant;
    halfmove = hist.halfmove;

    if(side == BLACK) {
        fullmove--;
    }

    if(hist.move.type & PROMOTION) {
        piece[hist.move.from] = PAWN;
    }
    else {
        piece[hist.move.from] = piece[hist.move.to];
    }
    color[hist.move.from] = side;
    if(hist.move.type & CAPTURE) {
        if(hist.move.type & EP_CAPTURE) {
            if(side == WHITE) {
                piece[hist.move.to + DOWN] = PAWN;
                color[hist.move.to + DOWN] = BLACK;
            }
            else {
                piece[hist.move.to + UP] = PAWN;
                color[hist.move.to + UP] = WHITE;
            }
            piece[hist.move.to] = EMPTY;
            color[hist.move.to] = EMPTY;
        }
        else {
            piece[hist.move.to] = hist.capture;
            color[hist.move.to] = xside;
        }
    }
    else {
        piece[hist.move.to] = EMPTY;
        color[hist.move.to] = EMPTY;
    }

    if(hist.move.type & CASTLE) {
        if(hist.move.to > hist.move.from) {
            if(side == WHITE) {
                piece[H1] = piece[F1];
                color[H1] = WHITE;
                piece[F1] = EMPTY;
                color[F1] = EMPTY;
            }
            else {
                piece[H8] = piece[F8];
                color[H8] = BLACK;
                piece[F8] = EMPTY;
                color[F8] = EMPTY;
            }
        }
        else {
            if(side == WHITE) {
                piece[A1] = piece[D1];
                color[A1] = WHITE;
                piece[D1] = EMPTY;
                color[D1] = EMPTY;
            }
            else {
                piece[A8] = piece[D8];
                color[A8] = BLACK;
                piece[D8] = EMPTY;
                color[D8] = EMPTY;
            }
        }
    }
    
}

u64 Perft(int depth) {

    if(depth == 0) {
        return 1ULL;
    }

    u64 nodes = 0;

    gen_moves();

    for(int m = 0; m < n_moves[ply]; m++) {
        if(make_move(move_list[ply][m])) {
            nodes += Perft(depth - 1);
            take_back();
        }
    }

    return nodes;
}
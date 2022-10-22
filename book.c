#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

bool open_book()
{
    book_file = fopen(BOOK_FILENAME, "r");
    if (book_file == NULL)
    {
        return FALSE;
    }
    return TRUE;
}

void close_book()
{
    if (book_file != NULL)
    {
        fclose(book_file);
        book_file = NULL;
    }
}

move_t book_move()
{
    move_t move;
    char line[MAX_INPUT_LENGTH];
    char book_line[MAX_INPUT_LENGTH];
    move_t book_list[MAX_BOOK_MOVES];
    int book_count[MAX_BOOK_MOVES];
    int line_length = 0;
    int n_moves = 0;
    int total_lines = 0;

    move.type = NO_MOVE;

    if (book_file == NULL)
    {
        return move;
    }

    for (int h = 0; h < hply; h++)
    {
        line_length += sprintf(line + line_length, "%s ", move_to_lan(history[h].move));
    }

    rewind(book_file);
    while (fgets(book_line, MAX_INPUT_LENGTH, book_file) != NULL)
    {
        if (!strncmp(line, book_line, line_length))
        {
            int m;
            move = lan_to_move(book_line + line_length);
            if (move.type & (NO_MOVE | ILLEGAL_MOVE))
            {
                continue;
            }
            for (m = 0; m < n_moves; m++)
            {
                if (book_list[m].from == move.from && book_list[m].to == move.to && book_list[m].prom == move.prom)
                {
                    book_count[m]++;
                    break;
                }
            }
            if (m == n_moves)
            {
                book_list[m] = move;
                book_count[m] = 1;
                n_moves++;
            }
            total_lines++;
        }
    }

    if (total_lines != 0)
    {
        int r = rand() % total_lines;
        for (int m = 0; m < n_moves; m++)
        {
            r -= book_count[m];
            if (r < 0)
            {
                return book_list[m];
            }
        }
    }

    return move;
}
#include <stdio.h>
#include "defs.h"

FILE *book;

bool open_book()
{
    book = fopen(BOOK_FILENAME, "r");
    if (book == NULL)
    {
        return FALSE;
    }
    return TRUE;
}

void close_book()
{
    if (book != NULL)
    {
        fclose(book);
    }
    book = NULL;
}

move_t book_move()
{
    move_t move;



    return move;
}
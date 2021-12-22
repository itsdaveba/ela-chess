SOURCE_FILES = \
	main.c \
	board.c \
	search.c \
	xboard.c \
	data.c

all: ela

ela: $(SOURCE_FILES) defs.h data.h protos.h
	gcc -O3 -o ela $(SOURCE_FILES)

clean:
	rm -f ela
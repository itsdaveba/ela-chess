SOURCE_FILES = \
	main.c \
	board.c \
	data.c

HEADER_FILES = \
	defs.h \
	data.h \
	protos.h

ela: $(SOURCE_FILES) $(HEADER_FILES)
	gcc -O3 -o ela $(SOURCE_FILES)

run: ela
	./ela

clean:
	rm -f *.out
	rm -f ela
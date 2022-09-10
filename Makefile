SOURCE_FILES = \
	main.c \
	board.c \
	data.c

HEADER_FILES = \
	defs.h \
	data.h \
	protos.h

random: $(SOURCE_FILES) $(HEADER_FILES)
	gcc -O3 -o random $(SOURCE_FILES)

run: random
	./random

clean:
	rm -f random
SOURCE_FILES = \
	main.c

all: clean ela run

ela: ${SOURCE_FILES}
	gcc -O3 -o ela ${SOURCE_FILES}

run: ela
	./ela

clean:
	rm -f *.out
	rm -f ela
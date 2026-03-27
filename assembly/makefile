all: cam_ascii

cam_ascii: cam_ascii.o
	ld -o cam_ascii cam_ascii.o

cam_ascii.o: main.asm
	as -o cam_ascii.o main.asm

run: cam_ascii
	./cam_ascii

clean:
	rm -f cam_ascii cam_ascii.o
/* 
Camera to Ascii
by Gustavo Piaz
*/


.equ ROW_STEP, 2
.equ COL_STEP, 1

.equ SYS_READ,      0
.equ SYS_WRITE,     1
.equ SYS_OPEN,      2
.equ SYS_CLOSE,     3
.equ SYS_MMAP,      9
.equ SYS_IOCTL,     16
.equ SYS_EXIT,      60

.equ STDOUT,        1

.equ O_RDWR,        2

.equ PROT_READ,     1
.equ MAP_SHARED,    1

.equ VIDIOC_S_FMT,      0xc0d05605
.equ VIDIOC_REQBUFS,    0xc0145608
.equ VIDIOC_QUERYBUF,   0xc0585609
.equ VIDIOC_QBUF,       0xc058560f
.equ VIDIOC_DQBUF,      0xc0585611
.equ VIDIOC_STREAMON,   0x40045612

.equ V4L2_BUF_TYPE_VIDEO_CAPTURE, 1
.equ V4L2_MEMORY_MMAP,            1
.equ V4L2_PIX_FMT_YUYV,          0x56595559

.equ CAP_WIDTH,   160
.equ CAP_HEIGHT,  120

.equ OUT_COLS,    CAP_WIDTH
.equ OUT_ROWS,    CAP_HEIGHT

.equ FMT_TYPE,       0
.equ FMT_WIDTH,      8
.equ FMT_HEIGHT,     12
.equ FMT_PIXFMT,    16

.equ BUF_INDEX,      0
.equ BUF_TYPE,       4
.equ BUF_MEMORY,    60
.equ BUF_OFFSET,    64
.equ BUF_LENGTH,    72

.section .data

toPrint: .string "Abrindo Camera...\n"
toPrintLen: .quad . - toPrint

dev_path:   .asciz "/dev/video0"
clrscr:     .ascii "\033[2J\033[H"
.equ CLRSCR_LEN, 7

palette:    .ascii " .,:;i1tfLCG08@"
.equ PALETTE_LEN, 15

.section .bss
.align 8
fmt_buf:    .space 208
reqbuf_buf: .space 16
qbuf_buf:   .space 96

mmap_ptr:   .quad 0
mmap_size:  .quad 0

out_line:   .space 256

.section .text
.global _start

_start:
	movq $SYS_WRITE,%rax
	movq $STDOUT, %rdi
	leaq toPrint(%rip),%rsi
	mov  toPrintLen(%rip), %rdx

	/* OPEN */
	movq $SYS_OPEN, %rax
	leaq dev_path(%rip), %rdi
	movq $O_RDWR, %rsi
	xorq %rdx, %rdx
	syscall
	movq %rax, %r15

	/* S_FMT */
	leaq fmt_buf(%rip), %rbx
	movl $V4L2_BUF_TYPE_VIDEO_CAPTURE, FMT_TYPE(%rbx)
	movl $CAP_WIDTH, FMT_WIDTH(%rbx)
	movl $CAP_HEIGHT, FMT_HEIGHT(%rbx)
	movl $V4L2_PIX_FMT_YUYV, FMT_PIXFMT(%rbx)

	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_S_FMT, %rsi
	movq %rbx, %rdx
	syscall

	/* REQBUFS */
	leaq reqbuf_buf(%rip), %rbx
	movl $1, (%rbx)
	movl $V4L2_BUF_TYPE_VIDEO_CAPTURE, 4(%rbx)
	movl $V4L2_MEMORY_MMAP, 8(%rbx)

	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_REQBUFS, %rsi
	movq %rbx, %rdx
	syscall

	/* QUERYBUF */
	leaq qbuf_buf(%rip), %rbx
	movl $0, BUF_INDEX(%rbx)
	movl $V4L2_BUF_TYPE_VIDEO_CAPTURE, BUF_TYPE(%rbx)
	movl $V4L2_MEMORY_MMAP, BUF_MEMORY(%rbx)

	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_QUERYBUF, %rsi
	movq %rbx, %rdx
	syscall

	movl BUF_LENGTH(%rbx), %eax
	movq %rax, mmap_size(%rip)
	movl BUF_OFFSET(%rbx), %r14d

	/* MMAP */
	movq $SYS_MMAP, %rax
	xorq %rdi, %rdi
	movq mmap_size(%rip), %rsi
	movq $PROT_READ, %rdx
	movq $MAP_SHARED, %r10
	movq %r15, %r8
	movq %r14, %r9
	syscall
	movq %rax, mmap_ptr(%rip)

	/* QBUF inicial */
	leaq qbuf_buf(%rip), %rbx
	movl $0, BUF_INDEX(%rbx)
	movl $V4L2_BUF_TYPE_VIDEO_CAPTURE, BUF_TYPE(%rbx)
	movl $V4L2_MEMORY_MMAP, BUF_MEMORY(%rbx)

	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_QBUF, %rsi
	movq %rbx, %rdx
	syscall

	/* STREAMON */
	movl $V4L2_BUF_TYPE_VIDEO_CAPTURE, reqbuf_buf(%rip)
	leaq reqbuf_buf(%rip), %rbx

	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_STREAMON, %rsi
	movq %rbx, %rdx
	syscall

/* ========= LOOP ========= */
main_loop:

	/* DQBUF */
	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_DQBUF, %rsi
	leaq qbuf_buf(%rip), %rdx
	syscall

	/* CLEAR */
	movq $SYS_WRITE, %rax
	movq $STDOUT, %rdi
	leaq clrscr(%rip), %rsi
	movq $CLRSCR_LEN, %rdx
	syscall

	/* RENDER */
	movq mmap_ptr(%rip), %rbp
	xorq %r12, %r12

row_loop:
	cmpq $OUT_ROWS, %r12
	jge render_done

	xorq %r13, %r13
	leaq out_line(%rip), %rdi

col_loop:
	cmpq $OUT_COLS, %r13
	jge end_col

	movq %r12, %rax
	imulq $CAP_WIDTH, %rax
	addq %r13, %rax
	shlq $1, %rax

	movzbq (%rbp,%rax), %rcx
	imulq $PALETTE_LEN, %rcx
	shrq $8, %rcx

	leaq palette(%rip), %rsi
	movb (%rsi,%rcx), %al
	movb %al, (%rdi)
	incq %rdi

	addq $COL_STEP, %r13
	jmp col_loop

end_col:
	movb $0x0a, (%rdi)
	incq %rdi

	leaq out_line(%rip), %rsi
	movq %rdi, %rdx
	subq %rsi, %rdx

	movq $SYS_WRITE, %rax
	movq $STDOUT, %rdi
	leaq out_line(%rip), %rsi
	syscall

	addq $ROW_STEP, %r12
	jmp row_loop

render_done:

	/* REQUEUE */
	movq $SYS_IOCTL, %rax
	movq %r15, %rdi
	movq $VIDIOC_QBUF, %rsi
	leaq qbuf_buf(%rip), %rdx
	syscall

	jmp main_loop
	
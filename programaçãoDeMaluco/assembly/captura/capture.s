# capture.s (Criação de função para C)
.intel_syntax noprefix

.equ ROW_STEP, 2
.equ COL_STEP, 1

# Chamadas de sistema e constantes (originais)
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
.global run_camera_capture_asm  # Tornar o nome da função global

run_camera_capture_asm:
	# Padrão de prólogo de função
	push rbp
	mov rbp, rsp

	# OPEN
	mov rax, SYS_OPEN
	lea rdi, [rip + dev_path]
	mov rsi, O_RDWR
	xor rdx, rdx
	syscall
	mov r15, rax  # FD no r15

	# S_FMT
	lea rbx, [rip + fmt_buf]
	mov dword ptr [rbx + FMT_TYPE], V4L2_BUF_TYPE_VIDEO_CAPTURE
	mov dword ptr [rbx + FMT_WIDTH], CAP_WIDTH
	mov dword ptr [rbx + FMT_HEIGHT], CAP_HEIGHT
	mov dword ptr [rbx + FMT_PIXFMT], V4L2_PIX_FMT_YUYV

	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_S_FMT
	mov rdx, rbx
	syscall

	# REQBUFS
	lea rbx, [rip + reqbuf_buf]
	mov dword ptr [rbx], 1
	mov dword ptr [rbx + 4], V4L2_BUF_TYPE_VIDEO_CAPTURE
	mov dword ptr [rbx + 8], V4L2_MEMORY_MMAP

	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_REQBUFS
	mov rdx, rbx
	syscall

	# QUERYBUF
	lea rbx, [rip + qbuf_buf]
	mov dword ptr [rbx + BUF_INDEX], 0
	mov dword ptr [rbx + BUF_TYPE], V4L2_BUF_TYPE_VIDEO_CAPTURE
	mov dword ptr [rbx + BUF_MEMORY], V4L2_MEMORY_MMAP

	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_QUERYBUF
	mov rdx, rbx
	syscall

	mov eax, dword ptr [rbx + BUF_LENGTH]
	mov [rip + mmap_size], rax
	mov r14d, dword ptr [rbx + BUF_OFFSET]

	# MMAP
	mov rax, SYS_MMAP
	xor rdi, rdi
	mov rsi, [rip + mmap_size]
	mov rdx, PROT_READ
	mov r10, MAP_SHARED
	mov r8, r15
	mov r9, r14
	syscall
	mov [rip + mmap_ptr], rax

	# QBUF inicial
	lea rbx, [rip + qbuf_buf]
	mov dword ptr [rbx + BUF_INDEX], 0
	mov dword ptr [rbx + BUF_TYPE], V4L2_BUF_TYPE_VIDEO_CAPTURE
	mov dword ptr [rbx + BUF_MEMORY], V4L2_MEMORY_MMAP

	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_QBUF
	mov rdx, rbx
	syscall

	# STREAMON
	mov dword ptr [rip + reqbuf_buf], V4L2_BUF_TYPE_VIDEO_CAPTURE
	lea rbx, [rip + reqbuf_buf]

	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_STREAMON
	mov rdx, rbx
	syscall

# ========= LOOP (LÓGICA ORIGINAL MANTERDADA) =========
main_loop:

	# DQBUF
	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_DQBUF
	lea rdx, [rip + qbuf_buf]
	syscall

	# CLEAR (Escrita para stdout)
	mov rax, SYS_WRITE
	mov rdi, STDOUT
	lea rsi, [rip + clrscr]
	mov rdx, CLRSCR_LEN
	syscall

	# RENDER (LÓGICA ORIGINAL)
	mov rbp, [rip + mmap_ptr]
	xor r12, r12 # ROW

row_loop:
	cmp r12, OUT_ROWS
	jge render_done

	xor r13, r13 # COL
	lea rdi, [rip + out_line]

col_loop:
	cmp r13, OUT_COLS
	jge end_col

	mov rax, r12
	imul rax, CAP_WIDTH
	add rax, r13
	shl rax, 1

	movzbq rcx, byte ptr [rbp + rax] # Pega Y
	imul rcx, PALETTE_LEN
	shr rcx, 8 # RCX = (Y * PALETTE_LEN) / 256

	lea rsi, [rip + palette]
	mov al, [rsi + rcx]
	mov [rdi], al
	inc rdi

	add r13, COL_STEP
	jmp col_loop

end_col:
	mov byte ptr [rdi], 0x0a # \n
	inc rdi

	lea rsi, [rip + out_line]
	mov rdx, rdi
	sub rdx, rsi # RDX = len(line)

	mov rax, SYS_WRITE
	mov rdi, STDOUT
	lea rsi, [rip + out_line]
	syscall

	add r12, ROW_STEP
	jmp row_loop

render_done:

	# REQUEUE
	mov rax, SYS_IOCTL
	mov rdi, r15
	mov rsi, VIDIOC_QBUF
	lea rdx, [rip + qbuf_buf]
	syscall

	# Como o Assembly tem um loop infinito (main_loop),
	# esta função nunca retornará a menos que você quebre o loop.
	# Para demonstração, mantivemos a lógica original.

	jmp main_loop

	# Padrão de epílogo de função (caso o loop seja quebrado)
	pop rbp
	ret
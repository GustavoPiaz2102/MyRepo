.section .data
	multiplicador: .long 130

.section .text

.global multiplicar

multiplicar:
	movl %edi, %eax
	movl multiplicador(%rip),%esi
	mull %esi
	ret

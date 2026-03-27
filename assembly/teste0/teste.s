.section .text

.global somar

somar:
	movl $0,%eax
	addl %edi,%eax
	addl %esi,%eax
	ret

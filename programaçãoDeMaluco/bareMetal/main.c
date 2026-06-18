/*
RCC - 0x4002 1000 - 0x4002 13FF
CRH - 0x04
BSRR - 0x10
RCC_APB2ENR - 0x18

CRH:
Reset value: 0x4444 4444
00: Input mode (reset state)
01: Output mode, max speed 10 MHz.
10: Output mode, max speed 2 MHz.
11: Output mode, max speed 50 MHz.
21 e 20 são MODE do PC13 [1,0] para 2 MHZ
23 e 22 são CNF do PC13 [0,0] para analog mode

BSRR:
Reset value: 0x0000 0000
PC13:
	BS13 - 13
	BR13 - 29

APB2ENR:
	IOPCEN - 4
*/

int main(void){
	volatile unsigned int *gpiocAddr = (unsigned int *)0x40011000;
	volatile unsigned int *rccAddr = (unsigned int *)0x40021000;
	volatile unsigned int *crhAddr = gpiocAddr + 0x04/4;
	volatile unsigned int *bsrrAddr = gpiocAddr + 0x10/4;
	volatile unsigned int *apb2enrAddr = rccAddr + 0x18/4;

	//Ligando o clock do GPIOC
	*apb2enrAddr |= (1<<4);

	//zerando o mode e o cnf
	*crhAddr |= (0xF<<20);
	*crhAddr ^= (0xF<<20);

	*crhAddr |= (2<<20); //10 para 2MHZ


	//setando o bit de set para 1
	//*bsrrAddr = (1<<13); // apaga o led pq a bluepill tem lógica invertida
	int i = 1;
	while(1){
		if(i == 250000) *bsrrAddr = (1<<13);
		if(i == 500000){
		*bsrrAddr = (1<<29);
		i = 1;
		}
		i++;
	}
	return 0;
}
/*

1111 0011 1111
or
0000 1111 0000
=
1111 1111 1111
xor
0000 1111 0000
=
1111 0000 1111
*/
#include <reg51.h>

void bcd_to_bin_int() {
	/* P1 contains a BCD */
	unsigned char bin, bcd;
	bin = (P1 >> 4) * 10 + (P1 & 0x0f);
	P2 = bin;

	bcd = (((bin / 10) % 10) << 4) | (bin % 10);
	P3 = bcd;
}

void bcd_to_bin_fixed_point() {
	/* P1 contains a BCD, convert it to binary bin_fixp = bin_int*2^n/10^m, n = 8, m = 2 */
	unsigned int bin;
	unsigned char bcd;
	bin = (P1 >> 4) * 10 + (P1 & 0x0f); /* binary integer */
	bin <<= 8; /* (*2^8) */
	bin = (bin % 100 > 50) ? bin / 100 + 1 : bin / 100; /* (/10^2 + rounding) */
	P2 = bin;

	bin *= 10; /* 0.ab -> a.b0 */
 	bcd = (bin & 0x0f00) >> 4; /* write a to the first place (0.a_) */
	bcd |= (((bin & 0xff) * 10) & 0xf00) >> 8; /* a.b0 -> b.00, write b to the second place (0.ab) */
	P3 = bcd;
}

int main() {
	if (P0 == 0) bcd_to_bin_int();
	else bcd_to_bin_fixed_point();
	return 0;
}
#include <stdio.h>

int main() {
	char nl[] = "\n", bs[] = "\\", dq[] = "\"";
	char e_nl[] = "\\n", e_bs[] = "\\\\", e_dq[] = "\\\"";
	char fmt[] = "#include <stdio.h>%s%sint main() {char nl[] = %s%s%s, bs[] = %s%s%s, dq[] = %s%s%s; char e_nl[] = %s%s%s%s, e_bs[] = %s%s%s%s, e_dq[] = %s%s%s%s; char fmt[] = %s%s%s; printf(fmt, nl, nl, dq, e_nl, dq, dq, e_bs, dq, dq, e_dq, dq, dq, bs, e_nl, dq, dq, e_bs, e_bs, dq, dq, e_bs, e_dq, dq, dq, fmt, dq, nl); return 0;}%s";
	printf(fmt, nl, nl, dq, e_nl, dq, dq, e_bs, dq, dq, e_dq, dq, dq, bs, e_nl, dq, dq, e_bs, e_bs, dq, dq, e_bs, e_dq, dq, dq, fmt, dq, nl);
	return 0;
}

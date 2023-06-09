/** Divide an arbitrarily large positive decimal integer (in "file.txt") by 190.
 * More generally, we could divide by any positive integer that is no larger than
 * a tenth of the maximum size_t.
 *
 * I am proud of the fact that this utilizes streaming to have constant space
 * complexity. I almost implemented a full BigInteger library (partially for fun)
 * to complete this challenge. This is much simpler. Both the input and output are
 * streamed immediately.
 *
 * Created for my application as an ESC180 2023/CSC190 2024 TA.
 *
 * Requires C99 or higher! This is because we print size_t and we use stdbool.h.
 *
 * NOTE: I do not support negative numbers. The file must only contain the
 * characters 0 to 9. A blank file will evaluate to 0.
 */

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>

#define FILE_NAME "file.txt"

int main() {
    int err = 0;
    int is_zero = true;
    size_t remainder = 0;
    const size_t divisor = 190;

    assert(divisor > 0 && "only positive divisors are supported!");

    /* Open file */
    FILE *fp = fopen(FILE_NAME, "r");
    assert(fp && "error opening file");

    for (int c = fgetc(fp); c != EOF; c = fgetc(fp)) {
        /* Assume digits char are ascending, consecutive numbers from 0 to 9 */
        assert('0' <= c && c <= '9' && "invalid decimal character!");
        remainder = 10 * remainder + (c - '0');
        if (remainder >= divisor) {
            size_t quotient = remainder / divisor;
            remainder -= quotient * divisor;
            printf("%zu", quotient);
            is_zero = false;
        } else if (is_zero) {
            /* Skip leading zeros from being displayed */
            continue;
        } else {
            printf("0");
        }
    }
    /* Print 0 if nothing has been printed yet - this will print 0 if the
     * numerator is less than the divisor or we have a blank file input. */
    if (is_zero) {
        printf("0");
    }
    printf("\n");

    /* Close file */
    err = fclose(fp);
    assert(!err && "error closing!");
    return 0;
}

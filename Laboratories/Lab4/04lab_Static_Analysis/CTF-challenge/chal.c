#include <stdio.h>
#include <string.h>
// gcc -g -o chal chal.c

int main() {
    puts("Welcome to our user email sweepstake!");
    puts("Only the 100th user gets a prize.");

    unsigned char count = 1;
    char email[32];

    while (1) {
        puts("Enter email: ");
        fgets(email, 31, stdin);
        email[strcspn(email, "\n")] = 0;

        if (count == 100) {
            printf("Congrats %s, you are the 100-th user (count=%d).\n", email, count);
        } else {
            printf("Sorry %s, you are not the 100-th user (count=%d). No prize for you.\n", email, count);
        }

        count++;
    }
}
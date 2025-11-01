#ifndef __STDIO_H__
#define __STDIO_H__

#define EOF -1
#define NUL 0
#define NULL (void *)0

int putchar(int c);
int puts(const char *s);
int printf(char *fmt,...);

#endif  /* __STDIO_H__ */

#include <stdarg.h>

extern char _dbuffer[1024];
static int dbuf_index = 0;

/* Ouput into a memory buffer for debugging in CPU simulation. */
int putchar(int c)
{
    _dbuffer[dbuf_index++] = (char)c;
    if (dbuf_index >= sizeof(_dbuffer))
        dbuf_index = 0;
    _dbuffer[dbuf_index] = 0;

    return c;
}

static void putstr(char *p)
{
    if(p) while(*p) putchar(*p++);
    else putstr("(NULL)");
}

int puts(char *p)
{
    putstr(p);
    return putchar('\n');
}

static void putnum(unsigned i, int base)
{
    char ascii[]="0123456789abcdef";
    char stack[32];
    int  ptr = 0;

    if(base==10)
    {
        int j = i;

        if(j<0)
        {
            putchar('-');
            i = -j;
        }
    }

    do
    {
        stack[ptr++] = ascii[(i%base)];
        i/=base;

        if(base!=10)
        {
            stack[ptr++] = ascii[(i%base)];
            i/=base;
        }
    }
    while(i);

    while(ptr) putchar(stack[--ptr]);
}

int printf(char *fmt,...)
{
    va_list ap;

    for(va_start(ap, fmt);*fmt;fmt++)
    {
        if(*fmt=='%')
        {
            fmt++;
            if(*fmt=='s') putstr(va_arg(ap,char *));
            else if(*fmt=='x') putnum(va_arg(ap,int),16);
            else if(*fmt=='d') putnum(va_arg(ap,int),10);
            else putchar(*fmt);
        }
        else putchar(*fmt);
    }

    va_end(ap);

    return 0;
}

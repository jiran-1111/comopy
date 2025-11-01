MEMORY
{
    MEM (rwx) : ORIGIN = 0x00000000, LENGTH = 0x2000
}
SECTIONS
{
    .text :
    {
        *boot*.o(.text)
        *boot*.o(.rodata)
        . = 512;
        _text = .;
        *(.text*)
        _etext = .;
    } > MEM
    .data :
    {
        _data = .;
        *(.rodata*)
        *(.data*)
        _global = . + 0x800;
        *(.sbss*)
        *(.bss*)
        *(.sdata*)
        *(.*)
        _edata = .;
    } > MEM
    .buffer (0x1000):
    {
        _dbuffer = .;
    }
    PROVIDE ( _stack = ORIGIN(MEM) + LENGTH(MEM) );
}

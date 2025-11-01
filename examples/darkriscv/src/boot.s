    .option pic
    .section .text
    .align 2
    .globl _start

_start:
    /* Initialize SoC and core. */

_call_main:
    la      sp,_stack
    la      gp,_global
    xor     a0,a0,a0    /* argc = 0 */
    xor     a1,a1,a1    /* argv = 0 */
    xor     a2,a2,a2    /* envp = 0 */
    call    main

infinite_loop:
    j       infinite_loop

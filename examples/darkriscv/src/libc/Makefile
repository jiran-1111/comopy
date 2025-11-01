
CFLAGS = -Wall -fcommon -ffreestanding -O2
CFLAGS += -march=$(ARCH) -mabi=$(ABI)
CFLAGS += -D__RISCV__ -DBUILD_DATE="\"$(DATE)\"" -DARCH="\"$(ARCH)\""
CFLAGS += -ffunction-sections -fdata-sections # enable this to make the FW smaller!
CFLAGS += -mcmodel=medany -mexplicit-relocs # relocable clode

ASFLAGS = -march=$(ARCH)
ARFLAGS = -rcs

PROJ = libc
OBJS = stdio.o softmath.o
ASMS = stdio.s softmath.s
SRCS = stdio.c softmath.c

DEPS = $(SRCS) $(ASMS) $(OBJS)

TARGETS = $(PROJ).a

.PHONY: all clean

all: $(DEPS) $(TARGETS)
	@echo sources ok for $(TARGETS).

clean:
	-rm -f $(OBJS) $(ASMS) $(PROJ).a

%.o: %.s Makefile
	$(AS) $(ASFLAGS) -c $< -o $@

%.s: %.c Makefile
	$(CC) $(CFLAGS) -S $< -o $@

%.a: $(OBJS) Makefile
	$(AR) $(ARFLAGS) $@ $(OBJS)
	$(RL) $@


CFLAGS = -Wall -fcommon -ffreestanding -O2
CFLAGS += -march=$(ARCH) -mabi=$(ABI) -I
CFLAGS += ../$(LIBC)/include
CFLAGS += -D__RISCV__ -DBUILD_DATE="\"$(DATE)\"" -DARCH="\"$(ARCH)\""
CFLAGS += -mcmodel=medany -mexplicit-relocs # relocable clode

ASFLAGS = -march=$(ARCH)
ARFLAGS = -rcs

PROJ = $(APP)
OBJS = $(APP).o
ASMS = $(APP).s
SRCS = $(APP).c

DEPS = $(SRCS) $(ASMS) $(OBJS)

TARGETS = $(PROJ).a

.PHONY: all clean

all: $(TARGETS) $(DEPS)
	@echo sources ok for $(TARGETS).

clean:
	-rm -f $(OBJS) $(ASMS) $(PROJ).a

%.o: %.s Makefile
	$(AS) $(ASFLAGS) -c $< -o $@

%.s: %.c Makefile
	$(CC) $(CFLAGS) -S $< -o $@

$(PROJ).a: $(OBJS) Makefile
	$(AR) $(ARFLAGS) $@ $(OBJS)
	$(RL) $@

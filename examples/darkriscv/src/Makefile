
SHELL := /bin/bash

export APP_PATH = applications
export APP = hello
export LIBC = libc

export ARCH = rv32i_zicsr
export ABI  = ilp32

# CCPATH: path to the cross compiler

export CROSS = riscv32-unknown-elf
export CC  = $(CCPATH)/$(CROSS)-gcc
export AS  = $(CCPATH)/$(CROSS)-as
export RL = $(CCPATH)/$(CROSS)-ranlib
export LD  = $(CCPATH)/$(CROSS)-ld
export OC  = $(CCPATH)/$(CROSS)-objcopy
export OD  = $(CCPATH)/$(CROSS)-objdump
export CPP = $(CCPATH)/$(CROSS)-cpp

export DATE = $(shell date -R)

CFLAGS = -Wall -fcommon -ffreestanding -O2
CFLAGS += -march=$(ARCH) -mabi=$(ABI)
CFLAGS += -D__RISCV__ -DBUILD_DATE="\"$(DATE)\"" -DARCH="\"$(ARCH)\""
ASFLAGS = -march=$(ARCH)
LDFLAGS = -T$(PROJ).ld -Map=$(PROJ).map -m elf32lriscv
LDFLAGS += -static -gc-sections --entry=_start # -Ttext=0
LDLIBS  = $(LIBS)

OCFLAGS = -O binary
ODFLAGS = -D

PROJ = darkriscv

LIBS = $(APP_PATH)/$(APP).a $(LIBC)/$(LIBC).a
OBJS = boot.o
ASMS = boot.s
# OBJS = boot_memcpy.o
# ASMS = boot_memcpy.s
SRCS =

DEPS = $(SRCS) $(ASMS) $(OBJS) $(PROJ).ld $(LIBS)
TARGETS = $(PROJ).mem
.PHONY: all subdirs clean

all: subdirs $(TARGETS) $(DEPS)
	@echo ok for $(TARGETS)

subdirs:
	$(MAKE) -C $(LIBC) all
	$(MAKE) -C $(APP_PATH) all

clean:
	$(MAKE) -C $(APP_PATH) clean
	$(MAKE) -C $(LIBC) clean
	-rm -f $(OBJS) $(PROJ).{S,map,bin,o,mem}

%.o: %.s Makefile
	$(AS) $(ASFLAGS) -c $< -o $@

%.s: %.c Makefile
	$(CC) $(CFLAGS) -S $< -o $@

$(PROJ).o: $(OBJS) $(PROJ).ld $(LIBS)
	$(RL) $(LDLIBS)
	$(LD) $(LDFLAGS) -o $@ $(OBJS) $(LDLIBS)
	$(OD) $(ODFLAGS) $@ > $(PROJ).S

$(PROJ).mem: $(PROJ).o
	$(OC) $(OCFLAGS) $< $(PROJ).bin
	hexdump -ve '1/4 "%08x\n"' $(PROJ).bin > $@
	wc -l $@

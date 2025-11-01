..
   ComoPy: Co-modeling tools for hardware generation with Python

   Copyright (C) 2024-2025 Microprocessor R&D Center (MPRC), Peking University
   SPDX-License-Identifier: MIT

   Author: Chun Yang

Data Types
##########


Bits
****

``Bits`` is the fundamental data type for fixed-width bit vectors in ComoPy.
It represents unsigned binary values and serves as the base type for all hardware data types.
All operations on ``Bits`` are performed with unsigned semantics.
During simulation, hardware signals are evaluated as ``Bits`` values, and all expressions operate on ``Bits`` data.


Construction
============

Convenient subclasses like ``b1``, ``b8``, ``b16``, ``b32`` are available for creating ``Bits`` constant values.
For example, ``b8(0xFF)`` corresponds to Verilog's ``8'hFF``.
``TRUE`` and ``FALSE`` are also defined as ``b1`` values for convenience.

These types and constants can be imported from ``comopy.bits``.


Signed values
=============

The ``.S`` property creates a signed view of a ``Bits`` value for signed operations.
Signed values are only allowed in signed comparisons, arithmetic right shifts, and signed extension.
Note that even signed operations still return unsigned ``Bits`` values.

ComoPy does not support implicit signed behavior. Signed semantics must be explicitly requested using the ``.S`` property, ensuring that signed operations are always clear and unambiguous in code.

**Example:**

.. code-block:: python

    class Shifter(RawModule):
        @build
        def build_all(s):
            s.in1 = Input(8)
            s.in2 = Input(8)
            s.out1 = Output(8)
            s.out2 = Output(8)
            s.out3 = Output(8)

            # Arithmetic right shift
            s.out1 @= s.in1.S >> 1
            s.out2 @= s.in2.S >> 1
            s.out3 @= (s.in1 + s.in2).S >> 2 if s.in1.S < s.in2.S else 0

.. note::
   The ``.S`` property creates a read-only signed view for signed operations only. It does not modify the original ``Bits`` value, which remains unchanged and unsigned.


Bit width
=========

The ``.W`` property returns the bit width of a ``Bits`` value as an integer, corresponding to Verilog's ``$bits()`` system function.
This value is a constant determined at design time, making it useful for parameterized designs.

The ``.N`` property returns the most significant bit of a ``Bits`` value as a ``b1`` result, which indicates whether a signed value is negative.
It is a shortcut for ``x[x.W - 1]``.

The ``.ext(width)`` method extends a ``Bits`` value to a wider bit width.
For unsigned values, it performs zero extension by padding with zeros.
For signed values (using ``.S.ext(width)``), it performs sign extension by replicating the sign bit.
To truncate to a narrower bit width, just use slicing (e.g., ``x[:4]`` for the lower 4 bits).


Indexing operations
===================


Reduction operations
====================

``Bits`` values provide reduction operations through property syntax that correspond to Verilog's unary reduction operators.
These properties perform bitwise reduction on all bits of a ``Bits`` value and return a single-bit ``b1`` result.

The following reduction properties are available:

* ``.AO`` - **A**\ ll **O**\ nes (reduction ``&`` in Verilog): Returns ``TRUE`` if all bits are 1, ``FALSE`` otherwise.
* ``.NZ`` - **N**\ ot **Z**\ ero (reduction ``|`` in Verilog): Returns ``TRUE`` if any bit is 1, ``FALSE`` if all bits are 0.
* ``.P`` - **P**\ arity (reduction ``^`` in Verilog): Returns ``TRUE`` if odd number of bits are 1, ``FALSE`` if even.
* ``.Z`` - **Z**\ ero (reduction ``~|`` in Verilog): Returns ``TRUE`` if all bits are 0, ``FALSE`` otherwise.

**Example:**

.. code-block:: python

    class Reductions(RawModule):
        @build
        def build_all(s):
            s.data = Input(8)
            s.all_ones = Output()
            s.any_one = Output()
            s.parity = Output()
            s.all_zeros = Output()

            s.all_ones @= s.data.AO  # Verilog: all_ones = &data
            s.any_one @= s.data.NZ   # Verilog: any_one = |data
            s.parity @= s.data.P     # Verilog: parity = ^data
            s.all_zeros @= s.data.Z  # Verilog: all_zeros = ~|data

.. note::
   All reduction operations return ``b1`` values, not Python booleans or integers.


BitPat
******

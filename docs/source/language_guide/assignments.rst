..
   ComoPy: Co-modeling tools for hardware generation with Python

   Copyright (C) 2024-2025 Microprocessor R&D Center (MPRC), Peking University
   SPDX-License-Identifier: MIT

   Author: Chun Yang

Assignment
##########


Assignment Operators
********************

ComoPy provides three distinct assignment operators, each designed for specific hardware modeling scenarios and corresponding to different Verilog constructs:

* ``@=`` for wire connections (structural)
* ``/=`` for blocking assignments (combinational behavior)
* ``<<=`` for non-blocking assignments (sequential behavior)


Wire connection (``@=``)
========================

The wire connection operator ``@=`` expresses structural connections in the circuit.
It is used within ``@build`` functions and translates directly to Verilog ``assign`` statements for continuous assignments.

**Example:**

.. code-block:: python

    class Adder(RawModule):
        @build
        def build_all(s):
            s.a = Input(8)
            s.b = Input(8)
            s.result = Output(8)
            s.result = s.a + s.b
            # Verilog: assign result = a & b;

**Drive Checking:**
The ``@=`` operator performs full compile-time drive checking.
Every bit of the target signal must have exactly one driver, with no unassigned (floating) bits.
Multiple ``@=`` statements targeting the same signal result in compilation errors.

**Restrictions:**

* The left-hand side of ``@=`` does not support variable indexing, including:

  - Variable-indexed bit selection: ``signal[variable_index]``
  - Variable-indexed part selection: ``signal[variable_base, width]``

.. note::
   In Verilog, ``assign`` statements require the left-hand side to be statically determinable at compile time.
   Variable indexing creates multiplexer logic that must be described in procedural blocks instead of continuous assignments.


Blocking assignment (``/=``)
============================


Non-blocking assignment (``<<=``)
=================================

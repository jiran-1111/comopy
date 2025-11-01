..
   ComoPy: Co-modeling tools for hardware generation with Python

   Copyright (C) 2024-2025 Microprocessor R&D Center (MPRC), Peking University
   SPDX-License-Identifier: MIT

   Author: Chun Yang

Control Flow
############

..
   TODO: Match/Case Statement Documentation

   Section: Match Statements (Python match mapped to SystemVerilog case)

   Design Principles:
   ==================
   1. No wildcards → always use "unique case" (parallel optimization)
   2. Has wildcards → always use "plain case" (sequential matching)
   3. Users MUST explicitly declare incomplete coverage intent with "case _: pass"

   Topics to cover:

   1. Basic Usage
      - Python match syntax maps to SystemVerilog case statement
      - Subject expression: must be a signal/wire (not constant, not loop var, not .W/.N)
      - Width inference from subject expression
      - Match statements MUST be exhaustive (must have case _)

   2. Supported Pattern Types
      - Integer literals: case 0:, case 1:, case 0xFF:
      - Bit pattern strings with don't-cares: case "10??":, case "1??0":
      - Default case: case _: (wildcard, must be present, can be empty with pass)

   3. Exhaustiveness Requirement (IMPORTANT!)
      - All match statements MUST have "case _:" branch
      - Two forms of default:
        * case _: <code>  → actual default logic
        * case _: pass    → explicit incomplete coverage (generates empty default)
      - Missing "case _:" → compilation error
      - Error message: "Match statement must be exhaustive. Add 'case _: pass' for incomplete coverage."

   4. Restrictions (comopy subset vs full Python match)
      - No variable capture: case x: or case 1 as x: NOT allowed
      - No guards: case 0 if condition: NOT allowed
      - No class patterns: case Bits(x): NOT allowed
      - No singleton patterns: case True:, case None: NOT allowed
      - No sequence patterns: case [1, 2]: NOT allowed
      - No mapping patterns: case {"key": value}: NOT allowed
      - No OR patterns: case 1 | 2: NOT allowed
      - Pattern values must fit in subject width

   5. Case Statement Types (mapped to SystemVerilog)
      - No wildcards → unique case (integer patterns only)
        * Always generates "unique case" regardless of coverage
        * ComoPy checks mutual exclusion
        * Synthesis tools optimize to parallel logic
      - Has wildcards → plain case (with ? patterns)
        * Generates plain "case" without qualifier
        * No mutual exclusion check (too complex)
        * Synthesis tools decide optimization strategy
      - Never use: unique0 (tool support inconsistent), priority (redundant)

   6. Completeness and Uniqueness Checking
      - Exhaustiveness: Must have "case _:" in all cases
      - Uniqueness (no wildcards only): All patterns must be distinct
      - For N-bit subject: 2^N possible values
      - Duplicate patterns detected and reported
      - With wildcards: overlap checking is user's responsibility

   7. Code Examples
      - Example 1: Complete coverage with default logic
        match value:
            case 0: x = 1
            case 1: x = 2
            case _: x = 0  # default has logic
        → unique case with "default: x = 0;"

      - Example 2: Incomplete coverage (HDLBits style)
        result = Unsigned[4](0)  # pre-initialize
        match opcode:
            case 0x01: result = 1
            case 0x02: result = 2
            case _: pass  # explicit incomplete coverage
        → unique case with "default: ;" (empty)

      - Example 3: With wildcards
        match value:
            case 0b10??: x = 1  # wildcard pattern
            case 0b01??: x = 2
            case _: x = 0
        → plain case (no qualifier)

      - Example 4: ERROR - missing default
        match value:  # ❌ ERROR
            case 0: x = 1
            case 1: x = 2
            # missing case _
        → Compilation error!

   8. SystemVerilog Translation
      - unique case: no wildcards, mutually exclusive patterns
        * Generated when: integer patterns only
        * Benefit: parallel logic optimization (mux)
        * Always has default (actual code or empty ";")
      - plain case: has wildcards, sequential matching
        * Generated when: ? patterns present
        * Behavior: first-match priority semantics
        * Synthesis tool decides if parallel possible
      - Never generated: unique0, priority case

   9. Best Practices
      - Prefer complete coverage: case _: <code> with actual logic
      - For HDLBits-style patterns:
        1. Pre-initialize variables before match
        2. Use "case _: pass" to explicitly declare intent
        3. Generates empty "default: ;" for tool compatibility
      - Avoid wildcards when possible (enables unique optimization)
      - Keep patterns mutually exclusive

   10. Common Errors and Solutions
       - ERROR: "Match statement must be exhaustive"
         → Add "case _: pass" (for incomplete) or "case _: <code>" (for complete)
       - ERROR: "Match cases must be mutually exclusive"
         → Ensure no duplicate patterns (when no wildcards)
       - Subject is constant → use if/elif instead
       - Pattern too wide → adjust pattern or widen subject
       - Guard usage → not supported, use nested if
       - Variable capture → not supported

   11. Comparison with SystemVerilog
       - Python match always maps to case (never if-elsif)
       - unique qualifier: parallel optimization, complete coverage
       - plain case: priority semantics, wildcard support
       - No unique0: tool support inconsistent (Quartus rejects, Verilator accepts)
       - No priority: redundant (plain case already has priority semantics)
       - casez: ComoPy uses plain case with ? (same as casez)

   12. Tool Compatibility Notes
       - Verilator: requires structural completeness (default present)
       - Quartus: rejects "unique0 case" with default
       - Empty default "default: ;" satisfies both tools
       - Pre-initialization before case does NOT satisfy tools
       - Solution: always generate default (actual or empty)

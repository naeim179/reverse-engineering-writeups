# First Reverse Engineering Write-up

## Challenge Info
- Name: CrackMe 01
- Category: Reverse Engineering
- Difficulty: Easy
- Platform: Windows x64

## Objective
Analyze the binary and recover the correct input.

## Tools Used
- Ghidra
- x64dbg
- strings

## Initial Analysis
The binary asks the user for a password and prints either success or failure.

## Static Analysis
Using Ghidra, I inspected the main function and followed the input validation logic.
I identified the comparison routine and checked the referenced strings.

## Dynamic Analysis
I opened the binary in x64dbg and placed breakpoints near the comparison code.
This helped confirm how the input was transformed before validation.

## Solution
The program applies a simple transformation to the input and compares it with the expected value.
After reversing the logic, the correct input was recovered.

## Flag / Result
`flag{example}`

## Lessons Learned
- Always inspect strings first
- Follow comparison functions carefully
- Static and dynamic analysis work best together

# ProblemFunctionSignature
The library for parsing the coding problem function signature.

String signature like `list[int32] f(a: list[list[str]], b:char)`
becomes an instance of `Signature`
with name `f`, `Type` of value it returns, and a list of `Argument`s,
each with its name and `Type`.

The code/files in the `problem_function_signature` directory and the `tests` directory should be synced with the same files in the [CodeStubGenerator](https://github.com/InterviewKickstart/CodeStubGenerator) repository with minor tweaks. Please review the diff once and check the diff of the previous commits/MRs to get a better understanding of what should be done and what should not be done.

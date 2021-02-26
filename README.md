# ProblemFunctionSignature
The library for parsing the coding problem function signature.

String signature like `list[int32] f(a: list[list[str]], b:char)`
becomes an instance of `Signature`
with name `f`, `Type` of value it returns, and a list of `Argument`s,
each with its name and `Type`.

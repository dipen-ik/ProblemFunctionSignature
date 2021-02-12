# ProblemFunctionSignature
The library for parsing the coding problem function signature.

String signature like `list[int32] f(a: list[list[str]])` becomes an instance of `Function`
with a name, (composite) `Type` and a list of `Argument`s, each with a name and a `Type`.

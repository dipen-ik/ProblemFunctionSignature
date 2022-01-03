import pytest

from problem_function_signature import signature as function
from problem_function_signature import type as t


A = function.Argument  # For brevity.


@pytest.mark.parametrize('input_func_signature, expected', [
    ('int32  fun1(a:int32 , b:  int32)',
     [('fun1', t.Type('int32')), A('a', t.Type('int32')), A('b', t.Type('int32'))]),

    ('list[int32] fun(z:list[list[char  ]])',
     [('fun', t.Type('list', t.Type('int32'))),
      A('z', t.Type('list', t.Type('list', t.Type('char'))))]),

    ('int32 fun(   )',
     [('fun', t.Type('int32'))]),

    ('LinkedListNode[int32] f(x: LinkedListNode[int32])',
     [('f', t.Type('LinkedListNode', t.Type('int32'))),
      A('x', t.Type('LinkedListNode', t.Type('int32')))]),

    ('list[LinkedListNode[int32]] f(x: list[LinkedListNode[int32]])',
     [('f', t.Type('list', t.Type('LinkedListNode', t.Type('int32')))),
      A('x', t.Type('list', t.Type('LinkedListNode', t.Type('int32'))))]),
])
def test_valid_function_signatures(input_func_signature, expected):
    func = function.parse(input_func_signature)
    result_simplified = [(func.name, func.type)] + func.args
    assert result_simplified == expected


@pytest.mark.parametrize(
    'uppercase, signature', [(uppercase, signature)
                             for uppercase in [False, True]
                             for signature in [
                                 'int32 X(y:int32)',
                                 'int32 x(Y:int32)',
                                 'int32 Fun(x:int32)',
                                 'int32 fUn(x:int32)',
                                 'int32 fun(xY:int32)',
                             ]
                             ])
def test_invalid_names_uppercase(uppercase, signature, request):
    def teardown():
        function.ALLOW_UPPERCASE_IN_NAMES = False

    request.addfinalizer(teardown)

    function.ALLOW_UPPERCASE_IN_NAMES = uppercase
    if uppercase:
        function.parse(signature)  # No error expected.
    else:
        with pytest.raises(function.InvalidNameException):
            function.parse(signature)


@pytest.mark.parametrize('signature', ['int32 fun(ab1:int32, 1bs:list[int32])',
                                       'int32 ?dsa(a:int32)',
                                       'int32 f_$(k:int32)',
                                       'int32 fun(a:int32, a:list[int32])',
                                       'int32 int64(a:int32)',
                                       'float f(float:str)',
                                       'int32 x(x:int32)',
                                       'int32 _a(x:int32)',
                                       'int32 x(_a:int32)',
                                       ])
def test_invalid_names(signature):
    with pytest.raises(function.InvalidNameException):
        function.parse(signature)


@pytest.mark.parametrize('signature',
                         ['int fun(x:list[int32])',
                          'int32 fun(x:list[int32, int32])',
                          'int32 fu n()',
                          'string x()',
                          'LinkedListNode[int32] f(y: LinkedListNode[int64])',
                          ])
def test_unsupported_types(signature):
    with pytest.raises(function.InvalidTypeException):
        function.parse(signature)


@pytest.mark.parametrize('signature', ['int32 fun(x)',
                                       'int32 fun(x:int32, y)',
                                       ])
def test_invalid_arguments(signature):
    with pytest.raises(function.ValidationException):
        function.parse(signature)

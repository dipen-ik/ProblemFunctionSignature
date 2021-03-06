import pytest

from problem_function_signature import type as tp


@pytest.mark.parametrize('data_type1, data_type2', [
    (tp.Type('int32'), tp.Type('int32')),

    (tp.Type('SinglyLinkedListNode', tp.Type('list', tp.Type('int32'))),
     tp.Type('SinglyLinkedListNode', tp.Type('list', tp.Type('int32')))),

    (tp.Type('list', tp.Type('list', tp.Type('int32'))),
     tp.Type('list', tp.Type('list',tp.Type('int32')))),
])
def test_equal_types(data_type1, data_type2):
    assert data_type1 == data_type2
    assert hash(data_type1) == hash(data_type2)


@pytest.mark.parametrize('data_type1, data_type2', [
    (tp.Type('int32'),
     tp.Type('float')),

    (tp.Type('SinglyLinkedListNode', tp.Type('list', tp.Type('str'))),
     tp.Type('SinglyLinkedListNode', tp.Type('list', tp.Type('int64')))),

    (tp.Type('list', tp.Type('list', tp.Type('int64'))),
     tp.Type('SinglyLinkedListNode', tp.Type('list', tp.Type('int64')))),

    (tp.Type('SinglyLinkedListNode', tp.Type('int32')),
     tp.Type('SinglyLinkedListNode', tp.Type('int64'))),

    (tp.Type('int32'), 'garbage'),
])
def test_unequal_types(data_type1, data_type2):
    """Checks whether two input types are the different."""
    assert data_type1 != data_type2


def test_validate_type():
    assert not tp.validate_type('lis[int32]')[0]
    assert not tp.validate_type('listt[int32]')[0]
    assert not tp.validate_type('list[int3]')[0]
    assert not tp.validate_type('list[int323]')[0]
    assert not tp.validate_type('list[int30]')[0]
    t = tp.validate_type('list[int32]')
    assert t[1]
    assert not t[0].primitive
    assert t[0].name == 'list'
    assert t[0].element_type.primitive
    assert t[0].element_type.name == 'int32'

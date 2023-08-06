from random import randint

import pytest

from mysqlsb.builder import MySQLStatementBuilder


def test_insert_statement():
    stmnt = MySQLStatementBuilder(None)
    val_a = randint(0, 100)
    val_b = randint(0, 100)
    val_c = randint(0, 100)
    stmnt.insert('test_table', ['col_a', 'col_b', 'col_c']).set_values([val_a, val_b, val_c])

    print("The query: ")
    print(stmnt.query)
    assert stmnt.query == 'INSERT INTO `test_table` (`col_a`, `col_b`, `col_c`) VALUES (%s, %s, %s) '
    assert stmnt.values == [val_a, val_b, val_c]


def test_insert_statement_multiple():
    stmnt = MySQLStatementBuilder(None)
    val_a = randint(0, 100)
    val_b = randint(0, 100)
    val_c = randint(0, 100)
    val_d = randint(0, 100)

    stmnt.insert('test_table', ['col_a', 'col_b'])
    stmnt.set_values([[val_a, val_b], [val_c, val_d]])

    assert stmnt.query == 'INSERT INTO `test_table` (`col_a`, `col_b`) VALUES (%s, %s), (%s, %s) '
    assert stmnt.values == [val_a, val_b, val_c, val_d]


def test_bad_insert_statement():
    stmnt = MySQLStatementBuilder(None)
    stmnt.insert('test_table', ['col_a', 'col_b', 'col_c'])

    with pytest.raises(TypeError):
        stmnt.set_values('a', 'b', 'c')

    with pytest.raises(TypeError):
        stmnt.set_values(1, 2, 3)

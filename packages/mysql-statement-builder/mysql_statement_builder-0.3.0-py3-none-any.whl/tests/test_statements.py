import mysqlsb.statements as stmnt


def test_create_insert_statement_backticks():
    s = stmnt.create_insert_statement('test_table', ['test_col_a', 'test_col_b'], backticks=True)
    assert s == "INSERT INTO `test_table` (`test_col_a`, `test_col_b`) "


def test_create_insert_statement_no_backticks():
    s = stmnt.create_insert_statement('test_table', ['test_col_a', 'test_col_b'], backticks=False)
    assert s == "INSERT INTO test_table (test_col_a, test_col_b) "


def test_values_array():
    s = stmnt.create_prepared_values_statement(3, 2)
    assert s == "VALUES (%s, %s, %s), (%s, %s, %s) "

import pytest
import sqlite3

from src.utils.error_handler import error_handler

def test_error_handler_positive(mocker) -> bool:
    demo_func = mocker.Mock(name = "demo_func")
    demo_func.return_value = "Decorator tested"
    wrapped = error_handler(demo_func)
    assert wrapped() == "Decorator tested"

def test_error_handler_negative(mocker) -> bool:
    demo_func = mocker.Mock(name = "demo_func")
    demo_func.side_effect = [
        sqlite3.IntegrityError,
        sqlite3.OperationalError,
        sqlite3.ProgrammingError,
        sqlite3.Error,
        ValueError,
        TypeError,
        Exception
    ]
    wrapped = error_handler(demo_func)
    for _ in range(7):
        assert wrapped() is None

from typing import Optional, Dict, Any

INCORRECT_TYPE_MSG = "Expected value with data type {expected_type} but got: {data_type}"
INCORRECT_LIST_ELEMENT_MSG = "Incorrect  data type at postion {position}: {msg}}"
INCORRECT_FIELD_TYPE_MSG = "Incorrect data type for field {key}: {msg}"

class DataError(Exception):
    exit_code = 1

    def __init__(self, msg: str, info: Optional[Dict[str, Any]]) -> None:
        self.msg = msg
        self.info = info


class IncorrectTypeError(DataError):
    def __init__(self, expected_type: str, actual_type: str):
        super().__init__(
            msg = f"Expected value with data type {expected_type} but got: {actual_type}"
            )


class IncorrectDateFormatError(DataError):
    def __init__(self, expected_format: str, actual_format: str):
        super().__ini__(
            msg = f"Excpected date format {expected_format} but got {actual_format}"
        )
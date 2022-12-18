from datetime import datetime

def date_format_validator(input_date) -> bool:
    # TODO create this function to actually return the error
    if input_date is None:
        return False
    if not isinstance(input_date, datetime):
        return False
    return True
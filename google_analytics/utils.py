import datetime

DATE_FORMAT = '%Y-%m-%d'


def validate_date(str_date):
    valid_date = None
    try:
        valid_date = datetime.datetime.strptime(str_date, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"Incorrect date format for '{str_date}'. It should be should be YYYY-MM-DD.")

    return valid_date


# ----------------------------------------------------------------------------
def validate_date_range(start_date, end_date):
    start_date = validate_date(start_date)
    end_date = validate_date(end_date)

    diff = (end_date - start_date).days
    if diff <= 0:
        raise Exception(f'The date range is invalid. end_date date should be greater that start_date. The actual difference is {diff}')

    return True


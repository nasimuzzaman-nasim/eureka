from datetime import datetime, date


def make_date(date_range_str):
    start = date.today()
    end = datetime.strptime(date_range_str, '%m/%d/%Y').date()
    return start, end
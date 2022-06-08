from datetime import datetime


def split_date(date_range_str):
    start_str, end_str = date_range_str.split(' - ')
    start = datetime.strptime(start_str, '%m/%d/%Y')
    end = datetime.strptime(end_str, '%m/%d/%Y')
    return start, end
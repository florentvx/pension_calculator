import datetime as dt

def date_string_to_date(input: str) -> dt.date:
    return dt.datetime.strptime(input, "%Y/%m/%d").date()

def get_month_id(date: dt.date, date_ref: dt.date):
    return date.month - date_ref.month + (date.year - date_ref.year) * 12 + (1 if date.day >= 25 else 0)

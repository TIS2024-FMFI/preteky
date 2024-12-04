from datetime import datetime
import calendar


def convert_month_to_number(month : str):
    try:
        if 0 < int(month) < 13:
            return int(month)
    except:
        return datetime.strptime(month, "%B").month


def return_date_with_last_day_of_month(month):
        month = convert_month_to_number(month)
        year = datetime.now().year
        last_day = calendar.monthrange(year, month)[1]
        return datetime(year, month, last_day).strftime("%Y-%m-%d")

def return_date_with_first_day_of_month(month):
    month = convert_month_to_number(month)
    year = datetime.now().year
    return datetime(year, month, 1).strftime("%Y-%m-%d")


def return_correct_format_of_date(year, month, day):
    return datetime(year, month, day).strftime("%Y-%m-%d")

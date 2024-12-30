from datetime import datetime
import calendar
from ErrorHandler import *


class DateConverter:
    def __init__(self):
        self.NUMBER_OF_MONTHS_IN_YEAR = 12

    def convert_to_google_calendar_format(self, date: str):
        """
        Convert date to Google Calendar format.
        :param date: Date in format 'yyyy-mm-dd'.
        :return: Tuple (start_time, end_time) in format 'yyyy-mm-ddTHH:MM:SS'.
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            start = f'{date}T08:00:00'
            end = f'{date}T20:00:00'
            return start, end
        except ValueError:
            raise ValueError("Date must be in format 'yyyy-mm-dd'.")

    def convert_month_to_number(self, month: str) -> int:
        """
        Convert name or number (in str) to number representation of the month.
        :param month: Mame (for example 'May') or number (for example '5').
        :return: Number of the month (int).
        """
        try:
            if month.isdigit() and 0 < int(month) <= self.NUMBER_OF_MONTHS_IN_YEAR:
                return int(month)
            else:
                return datetime.strptime(month, "%B").month
        except ValueError:
            raise ValueError("Name or number of month not valid.")

    def return_date_with_last_day_of_month(self, month: str) -> str:
        """
        Return date with last day of the month.
        :param month: Name of the month or number.
        :return: Date in form 'yyyy-mm-dd'.
        """
        month = self.convert_month_to_number(month)
        year = datetime.now().year
        last_day = calendar.monthrange(year, month)[1]
        return datetime(year, month, last_day).strftime("%Y-%m-%d")

    def return_date_with_first_day_of_month(self, month: str) -> str:
        """
        Return date with first day of month.
        :param month: Name or number of the month.
        :return: Date in format 'yyyy-mm-dd'.
        """
        month = self.convert_month_to_number(month)
        year = datetime.now().year
        return datetime(year, month, 1).strftime("%Y-%m-%d")

    def return_correct_format_of_date(self, year: int, month: int, day: int) -> str:
        """
        Return date in correct format.
        :param year: (int).
        :param month: (int).
        :param day: (int).
        :return: Formatted date 'yyyy-mm-dd'.
        """
        return datetime(year, month, day).strftime("%Y-%m-%d")

    def date_converter(self, date: str) -> str:
        """
        Convert date to format 'yyyy-mm-dd' or 'yyyy-mm-dd HH:MM'.
        :param date: Date in format 'yyyy-mm-dd' or 'yyyy-mm-dd HH:MM'.
        :return: Formatted date.
        """
        try:
            fmt = '%Y-%m-%d %H:%M' if ' ' in date else '%Y-%m-%d'
            return datetime.strptime(date, fmt).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Not valid. Expecting format 'yyyy-mm-dd' or 'yyyy-mm-dd HH:MM'.")

    def get_realtime_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def get_date_object_from_string(self, input_string: str):
        try:
            return datetime.strptime(input_string, "%Y-%m-%d")
        except ValueError:
            raise HandlerError("Wrong input string")


if __name__ == '__main__':
    dc = DateConverter()
    print("Google Calendar format:", dc.convert_to_google_calendar_format('2024-05-05'))
    print("Posledný deň v mesiaci:", dc.return_date_with_last_day_of_month('May'))
    print("Prvý deň v mesiaci:", dc.return_date_with_first_day_of_month('5'))
    print("Správny formát dátumu:", dc.return_correct_format_of_date(2024, 5, 15))
    print("Konverzia dátumu:", dc.date_converter('2024-05-05 10:30'))
    print(dc.get_realtime_date())

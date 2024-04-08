import json
import os
import datetime
from dataclasses import dataclass


@dataclass
class BookList:
	date: str
	category: str
	formatL: str
	URL: str


start_date = datetime.date(2011, 2, 13)
week = datetime.timedelta(days=7)


def get_booklists_with_URLs(date):
	date_string = str(date)
	date_string_with_slash = date_string.replace('-', '/')

	fiction_URL = f"https://www.nytimes.com/books/best-sellers/{date_string_with_slash}/combined-print-and-e-book-fiction/"
	nonfiction_URL = f"https://www.nytimes.com/books/best-sellers/{date_string_with_slash}/combined-print-and-e-book-nonfiction/"

	booklists = [
		BookList(date_string, 'fiction', 'all', fiction_URL),
		BookList(date_string, 'nonfiction', 'all', nonfiction_URL),
	]
	return booklists


def get_sundays():
	current_date = start_date
	today = datetime.date.today() - week
	dates = []
	while current_date < today:
		dates.append(current_date)
		current_date += week

	return dates


def main():
	sundays = get_sundays()
	for sunday in sundays:
		booklists = get_booklists_with_URLs(sunday)
		print(booklists)
		break


if __name__ == '__main__':
	main()

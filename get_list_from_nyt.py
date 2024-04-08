import json
import os
import datetime


start_date = datetime.date(2011, 2, 13)
week = datetime.timedelta(days=7)


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
	print(sundays)


if __name__ == '__main__':
	main()

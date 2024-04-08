import json
import os
import datetime
from dataclasses import dataclass

from bs4 import BeautifulSoup
import requests


@dataclass
class BookList:
	date: str
	category: str
	bookFormat: str
	URL: str

	@property
	def dirpath(self):
		return f"data/{self.date}"

	@property
	def json_name(self):
		return f"nytimes-booklist-{self.category}-{self.bookFormat}-{self.date}.json"

	@property
	def json_path(self):
		return os.path.join(self.dirpath, self.json_name)

	def download_json(self):
		if os.path.isfile(self.json_path):
			print(f"\tAlready downloaded: {self.json_path}")
			return

		books = get_book_list_from_URL(self.URL)
		jo = {}
		jo['books'] = books

		with open(self.json_path, 'w') as f:
			json.dump(jo, f, indent='\t', sort_keys=True)
		print(f"\tSaved: {self.json_path} ({len(books)} books)")


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


def get_book_list_from_URL(page_URL):
	response = requests.get(page_URL)
	soup = BeautifulSoup(response.text, 'lxml')

	article_tags = soup.find_all('article', attrs={'itemprop': 'itemListElement'})
	books = []
	for idx, article_tag in enumerate(article_tags):
		book = {}
		book['name'] = article_tag.find('h3', attrs={'itemprop': 'name'}).text.strip()
		book['author'] = article_tag.find('p', attrs={'itemprop': 'author'}).text.strip()
		book['publisher'] = article_tag.find('p', attrs={'itemprop': 'publisher'}).text.strip()
		book['description'] = article_tag.find('p', attrs={'itemprop': 'description'}).text.strip()

		book['rank'] = idx + 1
		book['imageSrc'] = article_tag.find('footer').find('img')['src']
		books.append(book)

	return books


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
	for sdx, sunday in enumerate(sundays):
		print(f"Sunday #{sdx+1} of {len(sundays)}: Date -> {sunday}")
		booklists = get_booklists_with_URLs(sunday)

		if not os.path.isdir(booklists[0].dirpath):
			os.mkdir(booklists[0].dirpath)
			print(f"Created directory: {booklists[0].dirpath}")

		for booklist in booklists:
			booklist.download_json()
		# break


if __name__ == '__main__':
	main()

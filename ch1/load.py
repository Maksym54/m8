import json
from mongoengine import connect
from models import Author, Quote

def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data.get('born_date'),
                born_location=author_data.get('born_location'),
                description=author_data.get('description')
            )
            author.save()

def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote = Quote(
                    tags=quote_data.get('tags', []),
                    author=author,
                    quote=quote_data.get('quote')
                )
                quote.save()

if __name__ == '__main__':

    connect('m8', host='mongo:27017')


    load_authors('authors.json')
    load_quotes('quotes.json')
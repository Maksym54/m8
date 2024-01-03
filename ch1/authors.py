from mongoengine import connect
from models import Quote, Author

def search_quotes(query_type, query_value):
    if query_type == 'name':
        author = Author.objects(fullname__icontains=query_value).first()
        if author:
            quotes = Quote.objects(author=author)
            return quotes
    elif query_type == 'tag':
        quotes = Quote.objects(tags__icontains=query_value)
        return quotes
    elif query_type == 'tags':
        tags = query_value.split(',')
        quotes = Quote.objects(tags__in=tags)
        return quotes
    else:
        return []

if __name__ == '__main__':
    connect('m8', host='mongo:27017')

    while True:
        user_input = input('Enter command (name, tag, tags, exit): ').split(':')
        if len(user_input) == 2:
            query_type, query_value = user_input[0], user_input[1].strip()
            result = search_quotes(query_type, query_value)
            for quote in result:
                print(f'Author: {quote.author.fullname}, Quote: {quote.quote}')
        elif user_input[0] == 'exit':
            break
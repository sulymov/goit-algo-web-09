from models import Author, Quote
import connect

# ***Обробка помилок при введенні даних***
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Value error! Try again!"
        except IndexError:
            return "Invalid command! Try again!"
        except KeyError:
            return "Key error! Try again!"
    return inner

# ***Парсинг даних***
@input_error
def parse_input(user_input):
        cmd, *args = user_input.split(":")
        cmd = cmd.strip().lower()
        args = [arg.strip() for arg in args]
        return cmd, *args

# ***Пошук цитат по автору***
@input_error    
def quotes_by_name(args):
    name, *_ = args
    author = Author.objects(fullname=name).first()
    print(f'--- All quotes by {name} ---')
    message = "This name doesn't exists."
    if author:
        quotes = Quote.objects(author=author)
        return "\n".join(q.quote for q in quotes)
    else:
        return message 
    
# ***Пошук цитат по одному тегу***
@input_error    
def quotes_by_tag(args):
    name, *_ = args
    quotes = Quote.objects(tags=name)
    print(f'--- All quotes by "{name}" ---')
    message = "This tag doesn't exists."
    if quotes:
        return "\n".join(q.quote for q in quotes)
    else:
        return message
    
# ***Пошук цитат по двох тегах***
@input_error    
def quotes_by_tags(args):
    tags = [t.strip() for t in args[0].split(",")]
    print(f'--- All quotes by "{', '.join(tags)}" ---')
    message = "These tags doesn't exists."
    quotes = Quote.objects(tags__in=tags)
    if quotes:
        return "\n".join(q.quote for q in quotes)
    else:
        return message

# ***Головна функція***
def main():
    print("Welcome to quote searching! Enter a command or enter 'exit' to finish!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == "exit":
            print("Good bye!")
            break
        
        elif command == "name":
            print(quotes_by_name(args))
                               
        elif command == "tag":
            print(quotes_by_tag(args))
        
        elif command == "tags":
            print(quotes_by_tags(args))
                    
        else:
            print("Invalid command. Try again!")

if __name__ == "__main__":
    main()
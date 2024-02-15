import string

def main():
    book_path = 'books/frakenstein.txt'
    document = read_doc(book_path)
    num_words = word_count(document)
    letter_counts = letter_count(document)
    sorted_counts = sort_counts(letter_counts)
    report(book_path, num_words, sorted_counts)

def sort_counts(letter_counts: dict[str, int]) -> list[dict[str, str | int]]:
    list_of_dicts: list[dict[str, int | str]] = []
    for key in letter_counts:
        item = {
            "letter": key,
            "count": letter_counts[key]
        }
        list_of_dicts.append(item)
    list_of_dicts.sort(reverse=True, key=sort_on)
    return list_of_dicts

def sort_on(dict):
    return dict["count"]

def report(book_path: str, num_words: int, letter_counts: list[dict[str, str | int]]) -> None:
    print(f"--- Begin report of {book_path} ---")
    print(f"There are {num_words} in the document")
    print(f"")
    for item in letter_counts:
        print(f"The '{item['letter']}' character was found {item['count']} times")
    print(f"")
    print(f"--- End report ---")

def read_doc(location: str) -> str:
    with open(location) as f:
        return f.read()

def word_count(document: str) -> int:
    words = document.split()
    return len(words)

def letter_count(document: str) -> dict[str, int]:
    letter_map: dict[str, int] = {}
    lowercase_letters: list[str] = list(string.ascii_lowercase)
    lowercase_document = document.lower()
    for letter in lowercase_letters:
        count = lowercase_document.count(letter)
        letter_map[letter] = count
    return letter_map


if __name__ == '__main__':
    main()

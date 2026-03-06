import json
import xml.etree.ElementTree as ET
from abc import abstractmethod, ABC


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class DisplayInterface(ABC):
    @abstractmethod
    def display(self, book: Book):
        pass


class ConsoleDisplay(DisplayInterface):
    def display(self, book: Book) -> None:
        print(book.content)


class ReverseDisplay(DisplayInterface):
    def display(self, book: Book) -> None:
        print(book.content[::-1])


class PrinterInterface(ABC):
    @abstractmethod
    def print_book(self, book: Book) -> None:
        pass


class ConsolePrinter(PrinterInterface):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrinter(PrinterInterface):
    def print_book(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class BookSerializer(ABC):
    """
    Цей абстрактний метод треба для того, щоб від нього можна було віднаслідувати
    скільки завгодно різних серіалайзерів. Він нічого не знає про книгу, лише приймає об'єкт
    книги.
    """
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class BookJSONSerializer(BookSerializer):
    """
    Серіалайзер для перетворення в json
    """
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class BookXMLSerializer(BookSerializer):
    """
    Серіалайзер для перетворення в XML
    """
    def serialize(self, book: Book) -> str:
        root = ET.Element("book")
        ET.SubElement(root, "title").text = book.title
        ET.SubElement(root, "content").text = book.content
        return ET.tostring(root, encoding="unicode")


def main(book: Book, commands: list[tuple[str, str]]) -> str | None:
    tools = {
        ("display", "console"): ConsoleDisplay(),
        ("display", "reverse"): ReverseDisplay(),
        ("print", "console"): ConsolePrinter(),
        ("print", "reverse"): ReversePrinter(),
        ("serialize", "json"): BookJSONSerializer(),
        ("serialize", "xml"): BookXMLSerializer(),
    }

    last_result = None

    for cmd_type, method_name in commands:
        tool = tools.get((cmd_type, method_name))

        if not tool:
            continue

        if isinstance(tool, DisplayInterface):
            tool.display(book)
        elif isinstance(tool, PrinterInterface):
            tool.print_book(book)
        elif isinstance(tool, BookSerializer):
            last_result = tool.serialize(book)

    return last_result


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")

    results = main(sample_book, [("display", "reverse"), ("serialize", "xml")])

    for res in results:
        print(f"Result: {res}")
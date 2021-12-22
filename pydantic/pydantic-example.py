import json
from typing import Optional, List
import pydantic


class ISBN10FormatError(Exception):

    def __init__(self, value:str, message:str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)

class ISBNMissingError(Exception):
    def __init__(self, title:str, message:str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)


class Book(pydantic.BaseModel):

    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    subtitle: Optional[str]

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_isbn10_or_isbn13(cls, values):
        if "isbn_10" not in values and "isbn_13" not in values:
            raise ISBNMissingError(
                title=values["title"],
                message="Document should have either an ISBN10 or ISBN13"
            )
        return values

    @pydantic.validator("isbn_10")
    @classmethod
    def isbn_10_valid(cls, value):
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ISBN10FormatError(value=value, message="ISBN10 should be 10 digits")

        def char_to_int(char:int) -> int:
            if char in "Xx":
                return 10
            return int(char)

        weighted_sum = sum((10 - i) * char_to_int(x) for i, x in enumerate(chars))
        if weighted_sum % 11 != 0:
            raise ISBN10FormatError(value=value, message="ISBN10 should be divisible by 11")

        return value

    class Config:
        allow_mutation = False
        anystr_lower = True

def main() -> None:

    with open("./data.json") as file:
        data = json.load(file)
        books: List[Book] = [Book(**item) for item in data]
        print(books[0])
        print(books[0].title)
        print(books[0].dict(exclude={"price"}))
        print(books[0].dict(include={"price"}))

if __name__ == "__main__":
    main()

from fastapi import Body, FastAPI


# creating new application of fastapi
app = FastAPI()


BOOKS = [
  {
    "title": "The Art of Simplicity",
    "author": "John Doe",
    "category": "Self-Help"
  },
  {
    "title": "Coding the Future",
    "author": "Jane Smith",
    "category": "Technology"
  },
  {
    "title": "Whispers in the Wind",
    "author": "Emily Hart",
    "category": "Fiction"
  },
  {
    "title": "Mindset Matters",
    "author": "Carol Greene",
    "category": "Psychology"
  },
  {
    "title": "Rust for Rustaceans",
    "author": "Steve Klabnik",
    "category": "Programming"
  },
  {
    "title": "Solana Unleashed",
    "author": "Parmesh R.",
    "category": "Blockchain"
  },
  {
    "title": "Design Thinking 101",
    "author": "Laura White",
    "category": "Design"
  },
  {
    "title": "The Startup Path",
    "author": "Elon F.",
    "category": "Entrepreneurship"
  },
  {
    "title": "History's Echo",
    "author": "Richard Lane",
    "category": "History"
  },
  {
    "title": "The Calm Coder",
    "author": "Mia Bennett",
    "category": "Technology"
  },
  {
    "title": "Digital Mindfulness",
    "author": "Sophie Clarke",
    "category": "Wellness"
  }
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# fetch a book using path parameter
@app.get("/books/get_book_by_author/")
async def get_book_by_author(author:str):
    book_to_send = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            book_to_send.append(book)
            break

    return book_to_send


# path parameters
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    my_book = []
    for book in BOOKS:
        if book_title.casefold() in book.get("title").casefold():
            my_book.append(book)

    if my_book == "":
        return "Sorry Book not found"
    else:
        return my_book


# query parameters
@app.get("/books/{title}/")
async def read_book_by_category(title: str, category: str):
    books = []
    for book in BOOKS:
        if category.casefold() in book.get("category").casefold():
            books.append(book)

    return {"books": books, "title": title}


# POST request method
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)


# PUT request method

@app.put("/books/update_book")
async def update_book(updated_book= Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("category").casefold() == updated_book.get("category").casefold():
            BOOKS[i] = updated_book

    return {"msg": f"Book {updated_book.get('title')} has been updated"}


# DELETE request method
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break




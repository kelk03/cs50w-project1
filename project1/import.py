from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv


engine = create_engine("postgresql://vubwftbaxwlciv:6781e79a9326371f458581b620a3501bbe09f323d59fecedfd9d2c37a10736f3@ec2-18-235-45-217.compute-1.amazonaws.com:5432/d8u04g900l54m0")
db = scoped_session(sessionmaker(bind=engine))

book = open("books.csv")
books = csv.reader(book)
print (books) 
i = 0

for isbn, title, author, year in books :
    if isbn == "isbn": 
        print ("Nos hemos saltado la primera linea");
    else: 
        i = i+1
        db.execute("Insert into books (isbn, title, author, year) values(:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author":author, "year":year} )
        print(f"Este es el libro numero {i}")
    db.commit()
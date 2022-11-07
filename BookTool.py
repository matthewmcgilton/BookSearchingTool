import requests
import json
import os
from tkinter import *

#Function to do an API request from ISBN in the first entrybox
def submit_ISBN():
    #Get ISBN from entry box and do API request
    isbn = e1.get()
    request = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
    response = requests.get(request)
    data = response.json()

    #Statement to see if API request is successful
    if(response.status_code == 200):
        #Try/except statements to make sure values exist, otherwise put in unknown
        try:
            title = data[f"ISBN:{isbn}"]['details']['title']
            update_entry(e2, title)
        except:
            update_entry(e2, "Unknown")
        try:
            author = data[f"ISBN:{isbn}"]['details']['authors'][0]['name']
            update_entry(e3, author)
        except:
            update_entry(e3, "Unknown")
        try:
            publisher = data[f"ISBN:{isbn}"]['details']['publishers'][0]
            update_entry(e4, publisher)
        except:
            update_entry(e4, "Unknown")
    else:
        print("API error")

#Function to update an entry box with a value as readonly
def update_entry(entry, value):
    entry.config(state=NORMAL)
    entry.delete(0, "end")
    entry.insert(0, value)
    entry.config(state=DISABLED)

#Function to save the search in the list and a json document
def save_book():
    value = ""
    json_value = {"ISBN": "Unknown",
                  "Title": "Unknown",
                  "Author": "Unknown",
                  "Publisher": "Unknown"}

    isbn = e1.get().replace(" ", "")
    title = e2.get()
    author = e3.get()
    publisher = e4.get()

    #Initial check to make sure book is new
    if any(book['ISBN'] == isbn for book in json.load(open('data.json'))['books']):
        print("Book already exists")
        return

    if isbn != "":
        json_value["ISBN"] = isbn
    if title != "Unknown" and title != "":
        value += f"{title},"
        json_value["Title"] = title
    if author != "Unknown" and author != "":
        value += f" {author},"
        json_value["Author"] = author
    if publisher != "Unknown" and publisher != "":
        value += f" {publisher}"
        json_value["Publisher"] = publisher
    
    if value != "":
        list1.insert("end", value)
        write_book(json_value)

#Function to write book to the JSON document
def write_book(new_book, path='data.json'):
    with open(path, 'r+') as f:
        data = json.load(f)
        data["books"].append(new_book)
        f.seek(0)
        json.dump(data, f, indent = 4)

#Window object
window = Tk()
window.geometry("475x175")
window.resizable(width=False, height=False)
window.title("Textbook Searching Tool")

#Lables for different sections
label = Label(window, text="ISBN")
label.grid(row=0, column=0)
label = Label(window, text="Title")
label.grid(row=0, column=2)
label = Label(window, text="Author")
label.grid(row=1, column=0)
label = Label(window, text="Publisher")
label.grid(row=1, column=2)

#Entry boxes for ISBN, title, author, and publisher
isbn = StringVar()
e1 = Entry(window, width=25, textvariable=isbn)
e1.grid(row=0, column=1)

title = StringVar()
e2 = Entry(window, width=25, textvariable=title, state=DISABLED)
e2.grid(row=0, column=3)

author = StringVar()
e3 = Entry(window, width=25, textvariable=author, state=DISABLED)
e3.grid(row=1, column=1)

publisher = StringVar()
e4 = Entry(window, width=25, textvariable=publisher, state=DISABLED)
e4.grid(row=1, column=3)

#List box (holds the saved books)
list1 = Listbox(window, height=7, width=45)
list1.grid(row=5, column=0, rowspan=4, columnspan=2)

#Scrollbar on list
scrollbar1 = Scrollbar(window, orient='horizontal')
scrollbar1.grid(row=11, column=0, columnspan=2)

scrollbar2 = Scrollbar(window)
scrollbar2.grid(row=5, column=2, rowspan=5)

list1.configure(xscrollcommand=scrollbar1.set)
list1.configure(yscrollcommand=scrollbar2.set)
scrollbar1.configure(command=list1.xview)
scrollbar2.configure(command=list1.yview)

#Buttons
button1 = Button(window, text="Search ISBN", width=16, command=submit_ISBN)
button1.grid(row=6, column=3)

button2 = Button(window, text="Add To List", width=16, command=save_book)
button2.grid(row=7, column=3)

#Checks for json file, creates default one if not, otherwise loads books in list
if not os.path.exists('data.json'):
    data = {"books":[]}
    json_file = json.dumps(data, indent=4)
    with open("data.json", "w") as f:
        f.write(json_file)
else:
    data = json.load(open('data.json'))
    for book in data['books']:
        value = ""
        title = book['Title']
        author = book['Author']
        publisher = book['Publisher']

        if title != "Unknown" and title != "":
            value += f"{title},"
        if author != "Unknown" and author != "":
            value += f" {author},"
        if publisher != "Unknown" and publisher != "":
            value += f" {publisher} "
        
        if value != "":
            list1.insert("end", value)

#Runs the window
window.mainloop()
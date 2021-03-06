# Capstone Project 1
# Library Management System

'''
Setup of database and initial library
'''
import sqlite3
db = sqlite3.connect('database/ebookstore_db')
cursor = db.cursor()

# Initial library contents set up as a Tuple to be transferred into books table
initialLibrary = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                  (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
                  (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
                  (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                  (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

# books table created to act as library database, initial library inserted into table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY,
    Title TEXT,
    Author TEXT,
    Qty INTEGER)
''')
db.commit()
cursor = db.cursor()
cursor.executemany('''
    INSERT OR REPLACE INTO books (id, Title, Author, Qty)
    VALUES (?,?,?,?)''', initialLibrary)
db.commit()

'''
Program user interface - set to run through all executable
functions as per userTask number selected
'''
userTask = int()
while userTask != "0":
    
    print("\n----------- NEW QUERY -----------")
    userTask = input("Please select 1 to 4 from the following list, or 0 to exit: \n1. Enter book\n2. Update book\n3. Delete book\n4. Search books\n0. Exit\n")


    if userTask == "1":         # Enter new book
        cursor.execute('''SELECT * FROM books WHERE id = (SELECT MAX(id) FROM books)''')    # Finds max ID and returns entire row to lastRow variable
        lastRow = cursor.fetchone()
        newID = lastRow[0] + 1  # New ID generated by adding 1 to max ID in table
        
        newTitle = input("Please type book title: ")
        newAuthor = input("Please type book author: ")
        newQty = input("Please type the number of copies to be kept in the library: ")
        cursor.execute('''INSERT INTO books (id, Title, Author, Qty)
            VALUES (?,?,?,?)''', (newID, newTitle, newAuthor, newQty))
        
    if userTask == "2":         # Update existing book
        cursor.execute('''SELECT * FROM books''')   # Print out library for user to select book ID to update
        for row in cursor:
            print('{0} | {1} | {2} | {3}'.format(row[0], row[1],row[2],row[3]))
        updateID = int(input("Please select the book you wish to update by typing the ID from the library list. An incorrect input will reset the query: "))

        cursor.execute('''SELECT id FROM books''')  # Confirm whether the selected ID is actually in the database
        listID = cursor.fetchall()
        for item in listID:
            if item[0] == updateID:
                cursor.execute('''SELECT * FROM books WHERE id = ?''', (updateID,))   # Book details captured as variables prior to updating
                updateBook = cursor.fetchone()
                updateTitle = updateBook[1]
                updateAuthor = updateBook[2]
                updateQty = updateBook[3]

                # User given the choice of which attribuute they want to update based on number selection
                updateNum = input("Select which attribute you wish to update by entering the corresponding number from 1 to 3: \n1. Title\n2. Author\n3. Qty\n: ")
                updateText = input("Type in the updated text: ")
                if updateNum == "1":
                    updateTitle = updateText
                elif updateNum == "2":
                    updateAuthor = updateText
                elif updateNum == "3":
                    updateQty = updateText
                        
                cursor.execute('''UPDATE books SET Title = ?, Author = ?, Qty = ? WHERE id = ? ''', (updateTitle, updateAuthor, updateQty, updateID))                

    if userTask == "3":        # Delete book entry from library
        cursor.execute('''SELECT * FROM books''')   # Print out library for user to select book ID to delete
        for row in cursor:
            print('{0} | {1} | {2} | {3}'.format(row[0], row[1],row[2],row[3]))
        deleteID = int(input("Please select the book you wish to delete by typing the ID from the library list: "))

        cursor.execute('''DELETE FROM books WHERE id = ?''', (deleteID,))

    if userTask == "4":         # Print library database to search books
        cursor.execute('''SELECT * FROM books''')   # Print out library for user to peruse
        for row in cursor:
            print('{0} | {1} | {2} | {3}'.format(row[0], row[1],row[2],row[3]))


#cursor.execute('''DROP TABLE books''')

db.close()


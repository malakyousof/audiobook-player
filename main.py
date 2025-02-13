import sys
import sqlite3
import pygame
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QHeaderView, QTableWidget,
    QTableWidgetItem, QMessageBox, QDialog, QPushButton, QSlider, QLabel,
    QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# Initialize pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()

def load_stylesheet(filename):
    try:
        with open(filename, "r") as file:
            stylesheet = file.read()
        return stylesheet
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return "fuck"


conn = sqlite3.connect('books.db')

cur = conn.cursor()

# Create a table for storing books (if it doesn't exist)
cur.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                file_path TEXT NOT NULL
            )''')

# Commit changes and close the connection
conn.commit()
conn.close()


###############################################################################################
def add_book(title, author, file_path):
    # Reconnect to the database
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()

    # Insert the book details into the books table
    cur.execute("INSERT INTO books (title, author, file_path) VALUES (?, ?, ?)", 
                (title, author, file_path))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Book '{title}' by {author} added successfully.")

############################################################################################################

def get_books():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    conn.close()
    return books
##########################################################################################################
class BookAdder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('add audiobook')
        self.resize(300,300)
        self.setWindowIcon(QIcon('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\audio-book.png'))            
        layout = QVBoxLayout()
        ###################################################
        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap('C:\\Users\\dell\OneDrive\\audioplayer\\images\\background-7234758_640.png')
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(self.rect())  # Make the label fill the window
        self.backgroundLabel.lower()   

        # Input fields
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText(' book title')
        layout.addWidget(self.title_input)
        
        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText(' book author')
        layout.addWidget(self.author_input)
        
        self.file_path_input = QLineEdit(self)
        self.file_path_input.setPlaceholderText(' file path')
        layout.addWidget(self.file_path_input)
        
        self.title_input.setObjectName("titleInput")
        self.author_input.setObjectName("authorInput")
        self.file_path_input.setObjectName("filepath")




        # Add book button
        add_button = QPushButton('Add audioBook', self)
        add_button.clicked.connect(self.add_book_to_db)
        layout.addWidget(add_button)
        


        self.setLayout(layout)
    
    def add_book_to_db(self):
        title = self.title_input.text()
        author = self.author_input.text()
        file_path = self.file_path_input.text()
        
        if title and author and file_path:
            add_book(title, author, file_path)
            self.title_input.clear()
            self.author_input.clear()
            self.file_path_input.clear()
########################################################################################################################
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMainWindow, QAction, QToolBar, QMessageBox, QDialog, QFormLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QIcon

class EditBookDialog(QDialog):
    def __init__(self, book_id, title, author, file_path, parent=None):
        super().__init__(parent)
        self.book_id = book_id
        self.initUI(title, author, file_path)
    
    def initUI(self, title, author, file_path):
        self.setWindowTitle('Edit Book')
        layout = QFormLayout()
        
        self.title_input = QLineEdit(title)
        layout.addRow('Title:', self.title_input)
        
        self.author_input = QLineEdit(author)
        layout.addRow('Author:', self.author_input)
        
        self.file_path_input = QLineEdit(file_path)
        layout.addRow('File Path:', self.file_path_input)
        
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
    
    def save_changes(self):
        title = self.title_input.text()
        author = self.author_input.text()
        file_path = self.file_path_input.text()
        if title and author and file_path:
            update_book(self.book_id, title, author, file_path)
            self.accept()

def update_book(book_id, title, author, file_path):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, file_path=? WHERE id=?", 
                (title, author, file_path, book_id))
    conn.commit()
    conn.close()

class LibraryViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Your Library')
        self.resize(600, 400)
        self.setWindowIcon(QIcon('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\icons8-audiobook-64.png'))      
        layout = QVBoxLayout()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Title', 'Author', 'File Path','play'])
        layout.addWidget(self.table)
        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\backiee-248850-landscape.jpg')
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(self.rect())  # Make the label fill the window
        self.backgroundLabel.lower()   


# Add a QLabel before each entry in the first column
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: lightgray;
                background-repeat: no-repeat;
                background-position: center;
                border: 1px solid pink;
                                 
            }
            QHeaderView::section {
            background-color: #6a4b8c;

            color: white;               
            border: 1px solid ;  
    }                    

        """)     
        
        self.load_books()
    


        # Create and add toolbar
        toolbar = QToolBar("My Toolbar")
        self.addToolBar(toolbar)
        edit_action = QAction(QIcon('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\edit-icon.png'), 'Delete Book', self)
        edit_action.triggered.connect(self.edit_book)
        toolbar.addAction(edit_action)

        delete_action = QAction(QIcon('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\delete-icon.png'), 'Edit Book', self)

        delete_action.triggered.connect(self.delete_book)
        toolbar.addAction(delete_action)

    
    def load_books(self):
        self.books = get_books()  # Store the book data as an instance variable
        self.table.setRowCount(len(self.books))
        for row, book in enumerate(self.books):
            for col, item in enumerate(book[1:]):  # Skip the id column
                self.table.setItem(row, col, QTableWidgetItem(item))
                play_button = QPushButton()
                play_button.setIcon(QIcon('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\icons8-play-50.png'))  # Replace with your play icon path
                play_button.clicked.connect(lambda checked, file_path=book[3]: self.play_audio(file_path))
                play_button.resize(5,5)
                self.table.setCellWidget(row, 3, play_button)
       
    def play_audio(self, file_path):
      self.playback_window = PlaybackWindow(file_path)
      self.playback_window.show()
    
    
  
    def edit_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id = get_books()[selected_row][0]
            title = self.table.item(selected_row, 0).text()
            author = self.table.item(selected_row, 1).text()
            file_path = self.table.item(selected_row, 2).text()

            dialog = EditBookDialog(book_id, title, author, file_path, self)
            if dialog.exec_():
                self.load_books()

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            book_id = get_books()[selected_row][0]
            reply = QMessageBox.question(self, 'Delete Book', 
                                         'Are you sure you want to delete this book?',
                                         QMessageBox.Yes | QMessageBox.No, 
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                delete_book(book_id)
                self.load_books()

def delete_book(book_id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
#####################################################################################################################
class PlaybackWindow(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a media player instance
        self.player = QMediaPlayer()

        # Set up media content
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.file_path)))

        # Create play/pause button
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.toggle_play)

        # Create a slider for the progress
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.change_position)

        layout.addWidget(self.play_button)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def toggle_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText('Play')
        else:
            self.player.play()
            self.play_button.setText('Pause')

    def change_position(self, value):
        self.player.setPosition(value * self.player.duration() / 100)
















 
#################################################################################################################
class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('homepage')
        self.resize(800 , 600)        
        self.setWindowIcon(QIcon('C:\\Users\\dell\\OneDrive\\audioplayer\\images\\download.png'))            

        self.backgroundLabel = QLabel(self)
        pixmap = QPixmap('C:\\Users\\dell\OneDrive\\audioplayer\\wallpaperflare.com_wallpaper (1).jpg')
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(self.rect())  # Make the label fill the window
        self.backgroundLabel.lower()  # Send the background label to the back  
        layout_main = QHBoxLayout()
        layout_buttons = QVBoxLayout()
        layout_buttons.addStretch()
#####################################################################################
        add_button_book = QPushButton('Add Audiobook', self)
        add_button_book.setObjectName('addAudiobookButton')
        add_button_book.clicked.connect(self.open_add_book)
        layout_buttons.addWidget(add_button_book)  # Add button to the vertical layout
        add_button_book.setFixedSize(200, 40)  
        layout_buttons.addWidget(add_button_book, alignment=Qt.AlignCenter)  # Align buttons centrally


        layout_buttons.addSpacing(40)  # Adjust this number to control the spacing between buttons


        view_button = QPushButton('Look at Library', self)
        view_button.setObjectName('LookatLibrary')

        view_button.clicked.connect(self.open_library)
        layout_buttons.addWidget(view_button)
        view_button.setFixedSize(200, 40)  # Set fixed size for buttons
        layout_buttons.addWidget(view_button, alignment=Qt.AlignCenter)

        layout_buttons.addStretch()
        layout_main.addLayout(layout_buttons)

        
    ################################################################################################

        # Container for the smaller image
        self.smallerImageLabel = QLabel(self)
        small_pixmap = QPixmap('C:\\Users\\dell\OneDrive\\audioplayer\\images\\lofti.jpg')  # Replace with the path to your smaller image
        self.smallerImageLabel.setPixmap(small_pixmap)
        self.smallerImageLabel.setScaledContents(True)
        self.smallerImageLabel.setFixedSize(320, 320)  # Adjust the size as needed
      
        # Center the smaller image in the middle
        layout_main.addWidget(self.smallerImageLabel, alignment=Qt.AlignCenter)
        ###################################################################################
                
        
        
        
        
        
        
        self.setLayout(layout_main)

  
         
    

#################################################################################################################
    def open_add_book(self):
        self.add_book_window = BookAdder()
        self.add_book_window.show()

    def open_library(self):
        self.library_window = LibraryViewer()
        self.library_window.show()
#################################################################################################
# Main execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylesheet = load_stylesheet("style.qss")
    app.setStyleSheet(stylesheet)
    main_window = MainPage()
    main_window.show()
    sys.exit(app.exec_())

# Define the main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("cozy reader")

        self.resize(800, 500)

        self.button = QPushButton("add audiobook", self)
        self.button.clicked.connect(self.on_click)

        # Set up a layout and add the button to it
        layout = QVBoxLayout()
        layout.addWidget(self.button)

        # Set the layout for the main window
        self.setLayout(layout)

    # Define the click event handler
    def on_click(self):
        self.button.setText("audiobook added to libary")

# Main function to run the application
if __name__ == "__main__":
    # Create an instance of the application
    app = QApplication(sys.argv)

    # Create an instance of the main window
    window = MainWindow()

    # Show the window
    window.show()
    pygame.mixer.Sound.play(window.music)
    # Run the application's event loop
    sys.exit(app.exec_())

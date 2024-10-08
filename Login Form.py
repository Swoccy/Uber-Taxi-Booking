import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        label = QLabel('Main App', parent=self)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        self.window_width, self.window_height = 600, 170
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Username')
        labels['Password'] = QLabel('Password')
        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['Username'],                                0, 0, 1, 1)
        layout.addWidget(self.lineEdits['Username'],                        0, 1, 1, 3)

        layout.addWidget(labels['Password'],                                1, 0, 1, 1)
        layout.addWidget(self.lineEdits['Password'],                        1, 1, 1, 3)

        loginbox = QHBoxLayout()
        button_login = QPushButton('&Log In', clicked=self.checkCredential)
        loginbox.addWidget(button_login)
        loginbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(loginbox,                                              2, 1, 2, 2)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red')
        layout.addWidget(self.status,                                           4, 0, 1, 3)

        # Initialize database connection
        self.init_database()

    def init_database(self):
        """
        Initialize the SQLite database and create the Customer table if it doesn't exist.
        """
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('Taxi_Sys.db')

        if not self.db.open():
            print("Unable to open database")
            return

        query = QSqlQuery()
        query.exec('''
            CREATE TABLE IF NOT EXISTS Customer (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL UNIQUE,
                Address TEXT NOT NULL,
                PNumber INTEGER UNIQUE CHECK (length(PNumber) >= 7),
                Email TEXT NOT NULL,
                Password TEXT NOT NULL,
                CardNo INTEGER NOT NULL
            )
        ''')

        # Insert the first sample user (for testing)
        query.prepare('''
            INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo)
            VALUES (:username, :address, :pnumber, :email, :password, :cardno)
        ''')
        query.bindValue(':username', 'Jack')
        query.bindValue(':address', 'Claude Neol Highway, Lowlands')
        query.bindValue(':pnumber', 6311043)
        query.bindValue(':email', 'JackLantern552@gmail.com')
        query.bindValue(':password', 'CanberryJuice')
        query.bindValue(':cardno', -9243)
        query.exec()

        query.prepare('''
            INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo)
            VALUES (:username, :address, :pnumber, :email, :password, :cardno)
        ''')
        query.bindValue(':username', 'Crain')
        query.bindValue(':address', 'Beckles Lane and Eastern Main Road, Arima')
        query.bindValue(':pnumber', 6670032)
        query.bindValue(':email', 'CucckooBirdsSuck1@gmail.com')
        query.bindValue(':password', 'SetItABlaze00')
        query.bindValue(':cardno', -8169)
        query.exec()

        query.prepare('''
            INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo)
            VALUES (:username, :address, :pnumber, :email, :password, :cardno)
        ''')
        query.bindValue(':username', 'Saint')
        query.bindValue(':address', '84-B Maraval Rd., Port Of Spain')
        query.bindValue(':pnumber', 6622975)
        query.bindValue(':email', 'IamSaintGermain@gmail.com')
        query.bindValue(':password', 'ThisDemonWillPerise')
        query.bindValue(':cardno', -9668)
        query.exec()

    def checkCredential(self):
        """
        Validate user credentials.
        """
        username = self.lineEdits['Username'].text()
        password = self.lineEdits['Password'].text()

        query = QSqlQuery()
        query.prepare('SELECT Password FROM Customer WHERE Username = :username')
        query.bindValue(':username', username)
        query.exec()

        if query.next():
            stored_password = query.value(0)
            if stored_password == password:
                time.sleep(1)
                self.mainApp = MainApp()
                self.mainApp.show()
                self.close()
            else:
                self.status.setText('Password is incorrect')
        else:
            self.status.setText('Username not found')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 25px;
        }
        QLineEdit {
            height: 200px;
        }
    ''')

    loginWindow = LoginWindow()
    loginWindow.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')

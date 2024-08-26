import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QVBoxLayout, \
    QHBoxLayout, QSizePolicy, QFormLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from Login import LoginWindow
from RegisterForm import RegisterWindow


class DriverServices(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("View Bookings")
        self.setFixedSize(800, 400)
        self.username = username

        layout = QFormLayout()
        self.setLayout(layout)

        self.lineEdits = {}
        self.lineEdits['CustomerID'] = QLineEdit()
        self.lineEdits['CustomerName'] = QLineEdit()
        self.lineEdits['PNumber'] = QLineEdit()
        self.lineEdits['Email'] = QLineEdit()
        self.lineEdits['Location'] = QLineEdit()
        self.lineEdits['Destination'] = QLineEdit()
        self.lineEdits['PickUpTime'] = QLineEdit()
        self.lineEdits['Returntime'] = QLineEdit()
        self.lineEdits['NumPassengers'] = QLineEdit()
        self.lineEdits['Payment type'] = QLineEdit()
        self.lineEdits['Payment amount'] = QLineEdit()


        self.lineEdits['CustomerID'].setPlaceholderText("1")
        self.lineEdits['CustomerName'].setPlaceholderText("Jack")
        self.lineEdits['PNumber'].setPlaceholderText("631-1043")
        self.lineEdits['Email'].setPlaceholderText("JackLantern552@gmail.com")
        self.lineEdits['Location'].setPlaceholderText("Claude Neol Highway, Lowlands")
        self.lineEdits['Destination'].setPlaceholderText("Port-Of-Spain")
        self.lineEdits['PickUpTime'].setPlaceholderText("13:00")
        self.lineEdits['ReturnTime'].setPlaceholderText("17:00")
        self.lineEdits['NumPassengers'].setPlaceholderText("5")
        self.lineEdits['[Payment Type'].setPlaceholderText("Card")
        self.lineEdits['Payment Amount'].setPlaceholderText("500.00")

        layout.addRow('CustomerID:', self.lineEdits['CustomerID'])
        layout.addRow('CustomerName:', self.lineEdits['CustomerName'])
        layout.addRow('PNumber:', self.lineEdits['PNumber'])
        layout.addRow('Email:', self.lineEdits['Email'])
        layout.addRow('Location:', self.lineEdits['Location'])
        layout.addRow('Destination:', self.lineEdits['Destination'])
        layout.addRow('Pick-Up Time:', self.lineEdits['PickUpTime'])
        layout.addRow('Return Time:', self.lineEdits['ReturnTime'])
        layout.addRow('Number of Passengers:', self.lineEdits['NumPassengers'])
        layout.addRow('Payment type:', self.lineEdits['PaymentType'])
        layout.addRow('Payment Amount:', self.lineEdits['PaymentAmount'])



        make_Accept_button = QPushButton('Accept Booking', clicked=self.Accept_booking)
        layout.addWidget(make_Accept_button)




    def Accept_booking(self):
        CustomerID = self.lineEdits['CustomerID'].text()
        Customername = self.lineEdits['CustomerName'].text()
        PNumber = self.lineEdits['PNumber'].text()
        Email=self.lineEdits['Email'].text()
        location = self.lineEdits['Location'].text()
        destination = self.lineEdits['Destination'].text()
        pick_up_time = self.lineEdits['PickUpTime'].text()
        return_time = self.lineEdits['ReturnTime'].text()
        num_passengers = self.lineEdits['NumPassengers'].text()
        Payment_type = self.lineEdits['Payment type'].text()
        Payment_amount = self.lineEdits['Payment amount'].text()

        class MainApp(QWidget):
            def __init__(self, username):
                super().__init__()
                self.registerWindow = None
                self.lineEdits = None
                self.username = username
                self.setWindowTitle("Main App")
                self.resize(500, 200)

                layout = QVBoxLayout()
                self.setLayout(layout)

                Viewbookings_button = QPushButton('ViewBookings')
                Viewbookings_button.clicked.connect(self.Viewbookings)
                layout.addWidget(Viewbookings_button)

            def Viewbookings(self):
                self.ViewbookingsWindow = self.ViewbookingsWindow(self.username)
                self.ViewbookingsWindow.show()

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

                layout.addWidget(labels['Username'], 0, 0, 1, 1)
                layout.addWidget(self.lineEdits['Username'], 0, 1, 1, 3)

                layout.addWidget(labels['Password'], 1, 0, 1, 1)
                layout.addWidget(self.lineEdits['Password'], 1, 1, 1, 3)

                loginbox = QHBoxLayout()
                login_button = QPushButton('&Log In', clicked=self.checkCredential)
                loginbox.addWidget(login_button)
                loginbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

                layout.addLayout(loginbox, 2, 0, 2, 2)

                register_button = QPushButton('Register', clicked=self.register_window)
                layout.addWidget(register_button, 2, 2, 2, 2)

                self.status = QLabel('')
                self.status.setStyleSheet('font-size: 25px; color: red')
                layout.addWidget(self.status, 4, 0, 1, 3)

                # Initialize database connection
                self.init_database()

                def register_window(self):
                    self.registerWindow = RegisterWindow()
                self.registerWindow.show()

                def init_database(self):
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

            query.prepare(
                '''INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo) VALUES (:username, :address, :pnumber, :email, :password, :cardno)''')
            query.bindValue(':username', 'Jack')
            query.bindValue(':address', 'Claude Neol Highway, Lowlands')
            query.bindValue(':pnumber', 6311043)
            query.bindValue(':email', 'JackLantern552@gmail.com')
            query.bindValue(':password', 'CanberryJuice')
            query.bindValue(':cardno', 9243)
            query.exec()

            query.prepare(
                '''INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo) VALUES (:username, :address, :pnumber, :email, :password, :cardno)''')
            query.bindValue(':username', 'Crain')
            query.bindValue(':address', 'Beckles Lane and Eastern Main Road, Arima')
            query.bindValue(':pnumber', 6670032)
            query.bindValue(':email', 'CucckooBirdsSuck1@gmail.com')
            query.bindValue(':password', 'SetItABlaze00')
            query.bindValue(':cardno', 8169)
            query.exec()

            query.prepare(
                '''INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo) VALUES (:username, :address, :pnumber, :email, :password, :cardno)''')
            query.bindValue(':username', 'Saint')
            query.bindValue(':address', '84-B Maraval Rd., Port Of Spain')
            query.bindValue(':pnumber', 6622975)
            query.bindValue(':email', 'IamSaintGermain@gmail.com')
            query.bindValue(':password', 'ThisDemonWillPerise')
            query.bindValue(':cardno', 9668)
            query.exec()

            query.exec('''
                    CREATE TABLE IF NOT EXISTS Booking (
                        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Location TEXT,
                        Destination TEXT,
                        PickUpTime TEXT,
                        ReturnTime TEXT,
                        NumPassengers INTEGER,
                        FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID)
                    )
                ''')

        def checkCredential(self):
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
                    self.mainApp = MainApp(username)
                    self.mainApp.show()
                    self.close()
                else:
                    self.status.setText('Password is incorrect')
            else:
                self.status.setText('Username not found')

    class RegisterWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Register")
            self.setFixedSize(600, 400)

            layout = QFormLayout()
            self.setLayout(layout)

            self.lineEdits = {}

            self.lineEdits['Username'] = QLineEdit()
            self.lineEdits['Address'] = QLineEdit()
            self.lineEdits['PNumber'] = QLineEdit()
            self.lineEdits['Email'] = QLineEdit()
            self.lineEdits['Password'] = QLineEdit()
            self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)
            self.lineEdits['CardNo'] = QLineEdit()

            layout.addRow('Username:', self.lineEdits['Username'])
            layout.addRow('Address:', self.lineEdits['Address'])
            layout.addRow('Phone Number:', self.lineEdits['PNumber'])
            layout.addRow('Email:', self.lineEdits['Email'])
            layout.addRow('Password:', self.lineEdits['Password'])
            layout.addRow('Card Number:', self.lineEdits['CardNo'])

            button_register = QPushButton('Register', clicked=self.register)
            layout.addWidget(button_register)

        def register(self):
            username = self.lineEdits['Username'].text()
            address = self.lineEdits['Address'].text()
            pnumber = self.lineEdits['PNumber'].text()
            email = self.lineEdits['Email'].text()
            password = self.lineEdits['Password'].text()
            cardno = self.lineEdits['CardNo'].text()

            if not (username and address and pnumber and email and password and cardno):
                QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
                return

            if not pnumber.isdigit() or not cardno.isdigit():
                QMessageBox.warning(self, "Input Error", "Phone Number and Card Number must be numeric.")
                return

            self.insert_data(username, address, int(pnumber), email, password, int(cardno))

        def insert_data(self, username, address, pnumber, email, password, cardno):
            if not QSqlDatabase.database().isOpen():
                QMessageBox.warning(self, "Error", "Database is not open.")
                return

            query = QSqlQuery()
            query.prepare('''
                    INSERT INTO Customer (Username, Address, PNumber, Email, Password, CardNo)
                    VALUES (:username, :address, :pnumber, :email, :password, :cardno)
                ''')
            query.bindValue(':username', username)
            query.bindValue(':address', address)
            query.bindValue(':pnumber', pnumber)
            query.bindValue(':email', email)
            query.bindValue(':password', password)
            query.bindValue(':cardno', cardno)

            if query.exec():
                QMessageBox.information(self, "Success", "Registration has been successful!")
                self.close()
            else:
                error_message = query.lastError().text()
                QMessageBox.warning(self, "Error", f"Registration has failed. Error: {error_message}")

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


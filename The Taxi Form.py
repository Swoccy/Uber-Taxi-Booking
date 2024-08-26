import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy, QFormLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


class MakeBooking(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Make a Booking")
        self.setFixedSize(800, 400)
        self.username = username

        layout = QFormLayout()
        self.setLayout(layout)

        self.lineEdits = {}
        self.lineEdits['Location'] = QLineEdit()
        self.lineEdits['Destination'] = QLineEdit()
        self.lineEdits['PickUpTime'] = QLineEdit()
        self.lineEdits['ReturnTime'] = QLineEdit()
        self.lineEdits['NumPassengers'] = QLineEdit()

        self.lineEdits['Location'].setPlaceholderText("Please enter your location")
        self.lineEdits['Destination'].setPlaceholderText("Please enter your destination")
        self.lineEdits['PickUpTime'].setPlaceholderText("yyyy-mm-dd HH:mm")
        self.lineEdits['ReturnTime'].setPlaceholderText("yyyy-mm-dd HH:mm")
        self.lineEdits['NumPassengers'].setPlaceholderText("Please enter the number of passengers")

        layout.addRow('Location:', self.lineEdits['Location'])
        layout.addRow('Destination:', self.lineEdits['Destination'])
        layout.addRow('Pick-Up Time:', self.lineEdits['PickUpTime'])
        layout.addRow('Return Time:', self.lineEdits['ReturnTime'])
        layout.addRow('Number of Passengers:', self.lineEdits['NumPassengers'])

        make_booking_button = QPushButton('Submit Booking', clicked=self.submit_booking)
        layout.addWidget(make_booking_button)

    def submit_booking(self):
        location = self.lineEdits['Location'].text()
        destination = self.lineEdits['Destination'].text()
        pick_up_time = self.lineEdits['PickUpTime'].text()
        return_time = self.lineEdits['ReturnTime'].text()
        num_passengers = self.lineEdits['NumPassengers'].text()

        if location and destination and pick_up_time and return_time and num_passengers:
            if not num_passengers.isdigit():
                QMessageBox.warning(self, "Input Error", "Number of passengers must be numeric.")
                return

            self.insert_booking(self.username, location, destination, pick_up_time, return_time, int(num_passengers))
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def insert_booking(self, username, location, destination, pick_up_time, return_time, num_of_passengers):

        query = QSqlQuery()
        query.prepare('SELECT CustomerID FROM Customer WHERE Username = :username')
        query.bindValue(':username', username)
        query.exec()

        if query.next():
            customer_id = query.value(0) # Retrieve the CustomerID

            query.prepare('''
               INSERT INTO Booking (Location, Destination, PickUpTime, ReturnTime, NumPassengers, CustomerID)
               VALUES (:location, :destination, :pickuptime, :returntime, :numofpassengers, :customerid)
           ''')

            query.bindValue(':location', location)
            query.bindValue(':destination', destination)
            query.bindValue(':pickuptime', pick_up_time)
            query.bindValue(':returntime', return_time)
            query.bindValue(':numofpassengers', num_of_passengers)
            query.bindValue(':customerid', customer_id)

            if query.exec():
                QMessageBox.information(self, "Booking", "Booking has been submitted successfully!")
                self.close()
            else:
                error_message = query.lastError().text()
                QMessageBox.warning(self, "Error", f"Failed to submit booking. Error: {error_message}")
        else:
            QMessageBox.warning(self, "Error", "404: User was not found")



class DeleteBooking(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        self.setLayout(layout)

        self.lineEdits = {}
        self.lineEdits['BookingID'] = QLineEdit()

        layout.addRow('Booking ID:', self.lineEdits['BookingID'])

        delete_booking_button = QPushButton('Delete Booking', clicked=self.delete_booking)
        layout.addWidget(delete_booking_button)

    def delete_booking(self):
        booking_id = self.lineEdits['BookingID'].text()
        if booking_id:

            QMessageBox.information(self, "Booking", "Booking has been deleted successfully!")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a booking ID.")


class UpdateBookingForm(QWidget):
    def __init__(self, booking_id):
        super().__init__()
        self.setWindowTitle("Update Booking")
        self.setFixedSize(800, 400)
        self.booking_id = booking_id

        layout = QFormLayout()
        self.setLayout(layout)

        self.lineEdits = {}
        self.lineEdits['Location'] = QLineEdit()
        self.lineEdits['Destination'] = QLineEdit()
        self.lineEdits['PickUpTime'] = QLineEdit()
        self.lineEdits['ReturnTime'] = QLineEdit()
        self.lineEdits['NumPassengers'] = QLineEdit()

        layout.addRow('Location:', self.lineEdits['Location'])
        layout.addRow('Destination:', self.lineEdits['Destination'])
        layout.addRow('Pick-Up Time:', self.lineEdits['PickUpTime'])
        layout.addRow('Return Time:', self.lineEdits['ReturnTime'])
        layout.addRow('Number of Passengers:', self.lineEdits['NumPassengers'])

        update_button = QPushButton('Update Booking', clicked=self.update_booking)
        layout.addWidget(update_button)

        self.load_booking_data()

    def load_booking_data(self):
        query = QSqlQuery()
        query.prepare('SELECT Location, Destination, PickUpTime, ReturnTime, NumPassengers FROM Booking WHERE BookingID = :booking_id')
        query.bindValue(':booking_id', self.booking_id)
        query.exec()

        if query.next():
            self.lineEdits['Location'].setText(query.value(0))
            self.lineEdits['Destination'].setText(query.value(1))
            self.lineEdits['PickUpTime'].setText(query.value(2))
            self.lineEdits['ReturnTime'].setText(query.value(3))
            self.lineEdits['NumPassengers'].setText(str(query.value(4)))
        else:
            QMessageBox.warning(self, "Error", "Booking ID not found.")
            self.close()

    def update_booking(self):
        location = self.lineEdits['Location'].text()
        destination = self.lineEdits['Destination'].text()
        pick_up_time = self.lineEdits['PickUpTime'].text()
        return_time = self.lineEdits['ReturnTime'].text()
        num_passengers = self.lineEdits['NumPassengers'].text()

        if location and destination and pick_up_time and return_time and num_passengers:
            if not num_passengers.isdigit():
                QMessageBox.warning(self, "Input Error", "Number of passengers must be numeric.")
                return

            query = QSqlQuery()
            query.prepare('''
                UPDATE Booking
                SET Location = :location,
                    Destination = :destination,
                    PickUpTime = :pickuptime,
                    ReturnTime = :returntime,
                    NumPassengers = :numofpassengers
                WHERE BookingID = :booking_id
            ''')
            query.bindValue(':location', location)
            query.bindValue(':destination', destination)
            query.bindValue(':pickuptime', pick_up_time)
            query.bindValue(':returntime', return_time)
            query.bindValue(':numofpassengers', int(num_passengers))
            query.bindValue(':booking_id', self.booking_id)

            if query.exec():
                QMessageBox.information(self, "Success", "Booking has been updated successfully!")
                self.close()
            else:
                error_message = query.lastError().text()
                QMessageBox.warning(self, "Error", f"Failed to update booking. Error: {error_message}")
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")


class EnterBookingID(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Booking ID")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.booking_id_edit = QLineEdit()
        self.booking_id_edit.setPlaceholderText("Enter Booking ID")
        layout.addWidget(self.booking_id_edit)

        ok_button = QPushButton('OK', clicked=self.open_update_form)
        layout.addWidget(ok_button)

    def open_update_form(self):
        booking_id = self.booking_id_edit.text()
        if booking_id.isdigit():
            self.update_form = UpdateBookingForm(int(booking_id))
            self.update_form.show()
            self.close()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid numeric Booking ID.")


class BookingsWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Bookings")
        self.resize(500, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        make_booking_button = QPushButton("Make Booking")
        delete_booking_button = QPushButton("Delete Booking")
        update_booking_button = QPushButton("Update Booking")

        layout.addWidget(make_booking_button)
        layout.addWidget(delete_booking_button)
        layout.addWidget(update_booking_button)

        make_booking_button.clicked.connect(self.show_make_booking)
        delete_booking_button.clicked.connect(self.show_delete_booking)
        update_booking_button.clicked.connect(self.show_enter_booking_id)

    def show_make_booking(self):
        self.make_booking = MakeBooking(self.username)
        self.make_booking.show()

    def show_delete_booking(self):
        self.delete_booking = DeleteBooking()
        self.delete_booking.show()

    def show_enter_booking_id(self):
        self.enter_booking_id = EnterBookingID()
        self.enter_booking_id.show()


class MainApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Main App")
        self.resize(500, 200)

        layout = QVBoxLayout()
        self.setLayout(layout)

        bookings_button = QPushButton('Bookings')
        bookings_button.clicked.connect(self.bookings)
        layout.addWidget(bookings_button)

    def bookings(self):
        self.bookingsWindow = BookingsWindow(self.username)
        self.bookingsWindow.show()


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
        login_button = QPushButton('&Log In', clicked=self.checkCredential)
        loginbox.addWidget(login_button)
        loginbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(loginbox,                                              2, 0, 2, 2)

        register_button = QPushButton('Register', clicked=self.register_window)
        layout.addWidget(register_button,                                       2, 2, 2, 2)

        self.status = QLabel('')
        self.status.setStyleSheet('font-size: 25px; color: red')
        layout.addWidget(self.status,                                           4, 0, 1, 3)

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
        
        query.prepare('''INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo) VALUES (:username, :address, :pnumber, :email, :password, :cardno)''')
        query.bindValue(':username', 'Jack')
        query.bindValue(':address', 'Claude Neol Highway, Lowlands')
        query.bindValue(':pnumber', 6311043)
        query.bindValue(':email', 'JackLantern552@gmail.com')
        query.bindValue(':password', 'CanberryJuice')
        query.bindValue(':cardno', 9243)
        query.exec()

        query.prepare('''INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo) VALUES (:username, :address, :pnumber, :email, :password, :cardno)''')
        query.bindValue(':username', 'Crain')
        query.bindValue(':address', 'Beckles Lane and Eastern Main Road, Arima')
        query.bindValue(':pnumber', 6670032)
        query.bindValue(':email', 'CucckooBirdsSuck1@gmail.com')
        query.bindValue(':password', 'SetItABlaze00')
        query.bindValue(':cardno', 8169)
        query.exec()

        query.prepare('''INSERT OR IGNORE INTO Customer (Username, Address, PNumber, Email, Password, CardNo) VALUES (:username, :address, :pnumber, :email, :password, :cardno)''')
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

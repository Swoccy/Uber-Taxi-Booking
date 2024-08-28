import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QSizePolicy, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

class ManagerMainApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Manager Main App")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        bookings_list_button = QPushButton('Customer Bookings')
        bookings_list_button.clicked.connect(self.bookings_list)
        layout.addWidget(bookings_list_button)

        staff_members_button = QPushButton('Staff Members')
        staff_members_button.clicked.connect(self.show_staff_members)
        layout.addWidget(staff_members_button)

        assign_drivers_button = QPushButton('Assign Drivers to Bookings')
        assign_drivers_button.clicked.connect(self.assign_drivers_to_bookings)
        layout.addWidget(assign_drivers_button)

    def bookings_list(self):
        self.bookingsListWindow = BookingsListWindow()
        self.bookingsListWindow.show()

    def show_staff_members(self):
        self.staffMembersWindow = StaffMembersWindow()
        self.staffMembersWindow.show()

    def assign_drivers_to_bookings(self):
        self.assignDriversWindow = AssignDriversWindow()
        self.assignDriversWindow.show()



class StaffMainApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Staff Main App")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        bookings_list_button = QPushButton('Customer Bookings')
        bookings_list_button.clicked.connect(self.bookings_List)
        layout.addWidget(bookings_list_button)

        staff_members_button = QPushButton('Staff Members')
        staff_members_button.clicked.connect(self.show_staff_members)
        layout.addWidget(staff_members_button)

        assign_drivers_button = QPushButton('Assign Drivers to Bookings')
        assign_drivers_button.clicked.connect(self.assign_drivers_to_bookings)
        layout.addWidget(assign_drivers_button)

    def bookings_list(self):
        self.bookingsListWindow = BookingsListWindow()
        self.bookingsListWindow.show()

    def show_staff_members(self):
        self.staffMembersWindow = StaffMembersWindow()
        self.staffMembersWindow.show()

    def assign_drivers_to_bookings(self):
        self.assignDriversWindow = AssignDriversWindow()
        self.assignDriversWindow.show()


class BookingsListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Bookings")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        self.customer_data()

    def customer_data(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["Customer ID", "Username", "Address", "PNumber", "Email", "Password", "CardNo"])

        query = QSqlQuery()
        query.exec('SELECT CustomerID, Username, Address, PNumber, Email, Password, CardNo FROM Customer')

        row = 0
        while query.next():
            self.tableWidget.insertRow(row)
            for column in range(7):
                item = QTableWidgetItem(str(query.value(column)))
                self.tableWidget.setItem(row, column, item)
            row += 1

class StaffMembersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Staff Members")
        self.resize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        self.staff_members_data()

    def staff_members_data(self):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Staff ID", "Username", "Phone Number", "Email", "Password", "Role"])

        query = QSqlQuery()
        query.exec('SELECT StaffNo, SUsername, SPNumber, SEmail, SPassword, Role FROM Staff')

        row = 0
        while query.next():
            self.tableWidget.insertRow(row)
            for column in range(6):
                item = QTableWidgetItem(str(query.value(column)))
                self.tableWidget.setItem(row, column, item)
            row += 1


class AssignDriversWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Assign Drivers to Bookings")
        self.resize(600, 400)

        layout = QFormLayout()
        self.setLayout(layout)

        self.bookingLineEdit = QLineEdit()
        self.driverLineEdit = QLineEdit()

        layout.addRow("Booking ID:", self.bookingLineEdit)
        layout.addRow("Driver Info:", self.driverLineEdit)

        assign_button = QPushButton("Assign", clicked=self.assign_driver_to_booking)
        layout.addWidget(assign_button)

        self.bookings_data()
        self.drivers_data()

    def bookings_data(self):
        query = QSqlQuery()
        query.exec('SELECT BookingID FROM Bookings')

        bookings = []
        while query.next():
            booking_id = query.value(0)
            bookings.append(str(booking_id))

        self.bookingLineEdit.setText(', '.join(bookings))

    def drivers_data(self):
        query = QSqlQuery()
        query.exec('SELECT StaffNo, SUsername FROM Staff WHERE Role = 1')  # Assuming Role = 1 means taxi driver

        drivers = []
        while query.next():
            driver_no = query.value(0)
            username = query.value(1)
            drivers.append(f"{driver_no} - {username}")

        self.driverLineEdit.setText(', '.join(drivers))

    def assign_driver_to_booking(self):

        booking_id = self.bookingLineEdit.text().strip()
        driver_info = self.driverLineEdit.text().strip()

        if not booking_id or not driver_info:
            QMessageBox.warning(self, "Input Error", "Please provide both Booking ID and Driver Info.")
            return

        driver_no = driver_info.split(' - ')[0]

        query = QSqlQuery()
        query.prepare('''UPDATE Bookings
                        SET StaffNo = :driver_no
                        WHERE BookingID = :booking_id''')

        query.bindValue(':driver_no', driver_no)
        query.bindValue(':booking_id', booking_id)

        if query.exec():
            QMessageBox.information(self, "Success", "Driver has been assigned to the booking successfully!")
        else:
            error_message = query.lastError().text()
            QMessageBox.warning(self, "Error", f"Failed to assign driver to the booking. Error: {error_message}")

class StaffLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Staff Login Window")
        self.setFixedSize(600, 170)

        layout = QGridLayout()
        self.setLayout(layout)

        labels = {}
        self.lineEdits = {}

        labels['SUsername'] = QLabel('Username')
        labels['SPassword'] = QLabel('Password')
        labels['SUsername'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['SPassword'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['SUsername'] = QLineEdit()
        self.lineEdits['SPassword'] = QLineEdit()
        self.lineEdits['SPassword'].setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(labels['SUsername'], 0, 0, 1, 1)
        layout.addWidget(self.lineEdits['SUsername'], 0, 1, 1, 3)

        layout.addWidget(labels['SPassword'], 1, 0, 1, 1)
        layout.addWidget(self.lineEdits['SPassword'], 1, 1, 1, 3)

        loginbox = QHBoxLayout()
        login_button = QPushButton('&Log In', clicked=self.check_staff_credential)
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
        self.staffRegisterWindow = StaffRegisterWindow()
        self.staffRegisterWindow.show()

    def init_database(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('Taxi_Sys.db')

        if not self.db.open():
            print("Unable to open database")
            return

        query = QSqlQuery()
        query.exec('''
            CREATE TABLE IF NOT EXISTS Staff (
                StaffNo INTEGER PRIMARY KEY AUTOINCREMENT,
                SUsername TEXT NOT NULL UNIQUE,
                SPNumber INTEGER UNIQUE CHECK (length(SPNumber) >= 7),
                SEmail TEXT NOT NULL,
                SPassword TEXT NOT NULL,
                Role INTEGER REFERENCES Role (RoleNo)
            )
        ''')

        query.exec('''
                CREATE TABLE IF NOT EXISTS Booking (
                    BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Location TEXT NOT NULL,
                    Destination TEXT NOT NULL,
                    PickUpTime TEXT NOT NULL,
                    ReturnTime TEXT NOT NULL,
                    NumPassengers INTEGER NOT NULL,
                    StaffNo INTEGER,
                    FOREIGN KEY(StaffNo) REFERENCES Staff(StaffNo)
                )
            ''')

    def check_staff_credential(self):
        username = self.lineEdits['SUsername'].text()
        password = self.lineEdits['SPassword'].text()

        query = QSqlQuery()
        query.prepare('SELECT SPassword, Role FROM Staff WHERE SUsername = :username')
        query.bindValue(':username', username)
        query.exec()

        if query.next():
            stored_password = query.value(0)
            role = query.value(1)
            if stored_password == password:
                time.sleep(1)
                if role == 1:  # Assuming Role = 1 is for staff
                    self.staffMainApp = StaffMainApp(username)
                    self.staffMainApp.show()
                elif role == 3:  # Assuming Role = 2 is for manager
                    self.managerMainApp = ManagerMainApp(username)
                    self.managerMainApp.show()
                self.close()
            else:
                self.status.setText('Password is incorrect')
        else:
            self.status.setText('Username not found')

class StaffRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Staff Register")
        self.setFixedSize(600, 400)

        layout = QFormLayout()
        self.setLayout(layout)

        self.lineEdits = {}

        self.lineEdits['SUsername'] = QLineEdit()
        self.lineEdits['SPNumber'] = QLineEdit()
        self.lineEdits['SEmail'] = QLineEdit()
        self.lineEdits['SPassword'] = QLineEdit()
        self.lineEdits['SPassword'].setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdits['Role'] = QLineEdit()

        layout.addRow('Username:', self.lineEdits['SUsername'])
        layout.addRow('Phone Number:', self.lineEdits['SPNumber'])
        layout.addRow('Email:', self.lineEdits['SEmail'])
        layout.addRow('Password:', self.lineEdits['SPassword'])
        layout.addRow('Role:', self.lineEdits['Role'])

        button_register = QPushButton('Register', clicked=self.register)
        layout.addWidget(button_register)

    def register(self):
        username = self.lineEdits['SUsername'].text()
        pnumber = self.lineEdits['SPNumber'].text()
        email = self.lineEdits['SEmail'].text()
        password = self.lineEdits['SPassword'].text()
        role = self.lineEdits['Role'].text()

        if not (username and pnumber and email and password and role):
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        if not pnumber.isdigit():
            QMessageBox.warning(self, "Input Error", "Phone Number must be in digits.")
            return

        self.insert_staff_data(username, int(pnumber), email, password, role)

    def insert_staff_data(self, username, pnumber, email, password, role):
        if not QSqlDatabase.database().isOpen():
            QMessageBox.warning(self, "Error", "Database is not open.")
            return

        query = QSqlQuery()
        query.prepare('''
            INSERT INTO Staff (SUsername, SPNumber, SEmail, SPassword, Role)
            VALUES (:username, :pnumber, :email, :password, :role)
        ''')
        query.bindValue(':username', username)
        query.bindValue(':pnumber', pnumber)
        query.bindValue(':email', email)
        query.bindValue(':password', password)
        query.bindValue(':role', role)

        if query.exec():
            QMessageBox.information(self, "Success", "Staff registration has been successful!")
            self.close()
        else:
            error_message = query.lastError().text()
            QMessageBox.warning(self, "Error", f"Staff registration has failed. Error: {error_message}")


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
    staff_login_window = StaffLoginWindow()
    staff_login_window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')

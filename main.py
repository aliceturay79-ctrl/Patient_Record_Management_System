import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QDialog,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QMessageBox
)

from PyQt6.QtCore import Qt, QDate

from database import connect_database


class PatientManagementSystem(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Patient Record Management System")
        self.setGeometry(200, 100, 1000, 650)

        self.create_dashboard()

    def create_dashboard(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        title = QLabel("PATIENT RECORD MANAGEMENT SYSTEM")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
            background-color: #1B5E20;
            padding: 25px;
        """)

        welcome = QLabel(
            "Welcome to the Patient Management Dashboard"
        )

        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        welcome.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            padding: 20px;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(welcome)

        buttons = [
            "Register Patient",
            "View Patients",
            "Manage Appointments",
            "Medical Records",
            "Prescriptions"
        ]

        for button_text in buttons:

            button = QPushButton(button_text)

            if button_text == "Register Patient":
                button.clicked.connect(self.register_patient)

            elif button_text == "View Patients":
                button.clicked.connect(self.view_patients)
                
            elif button_text == "Manage Appointments":
                button.clicked.connect(self.manage_appointments)

            elif button_text == "Medical Records":
                button.clicked.connect(self.medical_records)

            elif button_text == "Prescriptions":
                button.clicked.connect(self.prescriptions)



            button.setMinimumHeight(55)

            button.setStyleSheet("""
                font-size: 16px;
                background-color: #2E7D32;
                color: white;
                border-radius: 8px;
                padding: 10px;
            """)

            main_layout.addWidget(button)

        central_widget.setLayout(main_layout)

    def register_patient(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Register New Patient")
        dialog.setFixedSize(400, 350)

        layout = QFormLayout()

        first_name = QLineEdit()
        last_name = QLineEdit()

        date_of_birth = QDateEdit()
        date_of_birth.setCalendarPopup(True)
        date_of_birth.setDate(QDate.currentDate())

        gender = QComboBox()
        gender.addItems(["Male", "Female", "Other"])

        phone = QLineEdit()
        address = QLineEdit()

        layout.addRow("First Name:", first_name)
        layout.addRow("Last Name:", last_name)
        layout.addRow("Date of Birth:", date_of_birth)
        layout.addRow("Gender:", gender)
        layout.addRow("Phone:", phone)
        layout.addRow("Address:", address)

        save_button = QPushButton("Save Patient")
        layout.addWidget(save_button)

        def save_patient():

            if not first_name.text().strip() or not last_name.text().strip():

                QMessageBox.warning(
                    dialog,
                    "Missing Information",
                    "Please enter the patient's first and last name."
                )

                return

            connection = connect_database()

            if connection is None:

                QMessageBox.critical(
                    dialog,
                    "Database Error",
                    "Could not connect to the database."
                )

                return

            cursor = None

            try:

                cursor = connection.cursor()

                cursor.execute(
                    """
                    CALL register_patient(%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        first_name.text(),
                        last_name.text(),
                        date_of_birth.date().toPyDate(),
                        gender.currentText(),
                        phone.text(),
                        address.text()
                    )
                )

                connection.commit()

                QMessageBox.information(
                    dialog,
                    "Success",
                    "Patient registered successfully!"
                )

                dialog.accept()

            except Exception as error:

                connection.rollback()

                QMessageBox.critical(
                    dialog,
                    "Registration Error",
                    str(error)
                )

            finally:

                if cursor is not None:
                    cursor.close()

                connection.close()

        save_button.clicked.connect(save_patient)

        dialog.setLayout(layout)
        dialog.exec()

    def view_patients(self):

        connection = connect_database()

        if connection is None:

            QMessageBox.critical(
                self,
                "Database Error",
                "Could not connect to the database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    patient_id,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    phone,
                    address
                FROM patients
                ORDER BY patient_id
            """)

            patients = cursor.fetchall()

            if not patients:

                QMessageBox.information(
                    self,
                    "Patients",
                    "No patients registered yet."
                )

                return

            patient_details = ""

            for patient in patients:

                patient_details += (
                    f"ID: {patient[0]}\n"
                    f"Name: {patient[1]} {patient[2]}\n"
                    f"Date of Birth: {patient[3]}\n"
                    f"Gender: {patient[4]}\n"
                    f"Phone: {patient[5]}\n"
                    f"Address: {patient[6]}\n"
                    "-------------------------\n"
                )

            QMessageBox.information(
                self,
                "Registered Patients",
                patient_details
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )

        finally:

            if cursor is not None:
                cursor.close()

            connection.close()

    def manage_appointments(self):
    
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Appointments")
        dialog.setFixedSize(450, 350)

        layout = QFormLayout()

        patient_combo = QComboBox()
        doctor_combo = QComboBox()

        appointment_date = QDateEdit()
        appointment_date.setCalendarPopup(True)
        appointment_date.setDate(QDate.currentDate())

        status_combo = QComboBox()
        status_combo.addItems(["Scheduled", "Completed", "Cancelled"])

        connection = connect_database()

        if connection is None:
            QMessageBox.critical(
                self, "Database Error", "Could not connect to database."
            )
            return

        try:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT patient_id, first_name, last_name FROM patients"
            )
            patients = cursor.fetchall()

            cursor.execute(
                "SELECT doctor_id, doctor_name FROM doctors"
            )
            doctors = cursor.fetchall()

            for patient in patients:
                patient_combo.addItem(
                    f"{patient[1]} {patient[2]}",
                    patient[0]
                )

            for doctor in doctors:
                doctor_combo.addItem(
                    doctor[1],
                    doctor[0]
                )

            cursor.close()
            connection.close()

        except Exception as error:
            connection.close()
            QMessageBox.critical(self, "Error", str(error))
            return

        layout.addRow("Select Patient:", patient_combo)
        layout.addRow("Select Doctor:", doctor_combo)
        layout.addRow("Appointment Date:", appointment_date)
        layout.addRow("Status:", status_combo)

        save_button = QPushButton("Save Appointment")
        layout.addWidget(save_button)

        def save_appointment():

            if patient_combo.currentIndex() == -1 or doctor_combo.currentIndex() == -1:
                QMessageBox.warning(
                    dialog,
                    "Missing Information",
                    "Please register a patient and doctor first."
                )
                return

            connection = connect_database()

            if connection is None:
                QMessageBox.critical(
                    dialog, "Database Error", "Could not connect to database."
                )
                return

            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO appointments
                    (patient_id, doctor_id, appointment_date, appointment_status)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        patient_combo.currentData(),
                        doctor_combo.currentData(),
                        appointment_date.date().toPyDate(),
                        status_combo.currentText()
                    )
                )

                connection.commit()
                cursor.close()
                connection.close()

                QMessageBox.information(
                    dialog,
                    "Success",
                    "Appointment saved successfully!"
                )

                dialog.accept()

            except Exception as error:
                connection.rollback()
                cursor.close()
                connection.close()

                QMessageBox.critical(
                    dialog, "Appointment Error", str(error)
                )

        save_button.clicked.connect(save_appointment)

        dialog.setLayout(layout)
        dialog.exec()

    def medical_records(self):
    
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Medical Record")
        dialog.setFixedSize(450, 350)

        layout = QFormLayout()

        patient_combo = QComboBox()
        doctor_combo = QComboBox()

        diagnosis = QLineEdit()
        treatment = QLineEdit()

        record_date = QDateEdit()
        record_date.setCalendarPopup(True)
        record_date.setDate(QDate.currentDate())

        connection = connect_database()

        if connection is None:
            QMessageBox.critical(
                self, "Database Error", "Could not connect to database."
            )
            return

        try:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT patient_id, first_name, last_name FROM patients"
            )
            patients = cursor.fetchall()

            cursor.execute(
                "SELECT doctor_id, doctor_name FROM doctors"
            )
            doctors = cursor.fetchall()

            for patient in patients:
                patient_combo.addItem(
                    f"{patient[1]} {patient[2]}",
                    patient[0]
                )

            for doctor in doctors:
                doctor_combo.addItem(doctor[1], doctor[0])

            cursor.close()
            connection.close()

        except Exception as error:
            connection.close()
            QMessageBox.critical(self, "Error", str(error))
            return

        layout.addRow("Select Patient:", patient_combo)
        layout.addRow("Select Doctor:", doctor_combo)
        layout.addRow("Diagnosis:", diagnosis)
        layout.addRow("Treatment:", treatment)
        layout.addRow("Record Date:", record_date)

        save_button = QPushButton("Save Medical Record")
        layout.addWidget(save_button)

        def save_record():

            if not diagnosis.text().strip():
                QMessageBox.warning(
                    dialog,
                    "Missing Information",
                    "Please enter a diagnosis."
                )
                return

            connection = connect_database()

            if connection is None:
                QMessageBox.critical(
                    dialog, "Database Error", "Could not connect to database."
                )
                return

            cursor = None

            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO medical_records
                    (patient_id, doctor_id, diagnosis, treatment, record_date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        patient_combo.currentData(),
                        doctor_combo.currentData(),
                        diagnosis.text(),
                        treatment.text(),
                        record_date.date().toPyDate()
                    )
                )

                connection.commit()

                QMessageBox.information(
                    dialog,
                    "Success",
                    "Medical record saved successfully!"
                )

                dialog.accept()

            except Exception as error:
                connection.rollback()
                QMessageBox.critical(
                    dialog, "Medical Record Error", str(error)
                )

            finally:
                if cursor is not None:
                    cursor.close()
                connection.close()

        save_button.clicked.connect(save_record)

        dialog.setLayout(layout)
        dialog.exec()

    def prescriptions(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Prescription")
        dialog.setFixedSize(450, 300)

        layout = QFormLayout()

        patient_combo = QComboBox()
        doctor_combo = QComboBox()

        medication_name = QLineEdit()
        dosage = QLineEdit()

        prescription_date = QDateEdit()
        prescription_date.setCalendarPopup(True)
        prescription_date.setDate(QDate.currentDate())

        connection = connect_database()

        if connection is None:
            QMessageBox.critical(
                self, "Database Error", "Could not connect to database."
            )
            return

        try:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT patient_id, first_name, last_name FROM patients"
            )
            patients = cursor.fetchall()

            cursor.execute(
                "SELECT doctor_id, doctor_name FROM doctors"
            )
            doctors = cursor.fetchall()

            for patient in patients:
                patient_combo.addItem(
                    f"{patient[1]} {patient[2]}",
                    patient[0]
                )

            for doctor in doctors:
                doctor_combo.addItem(
                    doctor[1],
                    doctor[0]
                )

            cursor.close()
            connection.close()

        except Exception as error:
            connection.close()
            QMessageBox.critical(self, "Error", str(error))
            return

        layout.addRow("Select Patient:", patient_combo)
        layout.addRow("Select Doctor:", doctor_combo)
        layout.addRow("Medication Name:", medication_name)
        layout.addRow("Dosage:", dosage)
        layout.addRow("Prescription Date:", prescription_date)

        save_button = QPushButton("Save Prescription")
        layout.addWidget(save_button)

        def save_prescription():

            if not medication_name.text().strip() or not dosage.text().strip():
                QMessageBox.warning(
                    dialog,
                    "Missing Information",
                    "Please enter the medication name and dosage."
                )
                return

            connection = connect_database()

            if connection is None:
                QMessageBox.critical(
                    dialog,
                    "Database Error",
                    "Could not connect to database."
                )
                return

            cursor = None

            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO prescriptions
                    (
                        patient_id,
                        doctor_id,
                        medication_name,
                        dosage,
                        prescription_date
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        patient_combo.currentData(),
                        doctor_combo.currentData(),
                        medication_name.text(),
                        dosage.text(),
                        prescription_date.date().toPyDate()
                    )
                )

                connection.commit()

                QMessageBox.information(
                    dialog,
                    "Success",
                    "Prescription saved successfully!"
                )

                dialog.accept()

            except Exception as error:
                connection.rollback()

                QMessageBox.critical(
                    dialog,
                    "Prescription Error",
                    str(error)
                )

            finally:
                if cursor is not None:
                    cursor.close()

                connection.close()

        save_button.clicked.connect(save_prescription)

        dialog.setLayout(layout)
        dialog.exec()




def main():

    app = QApplication(sys.argv)

    window = PatientManagementSystem()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
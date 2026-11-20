CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    phone VARCHAR(20),
    address VARCHAR(150),
    registration_date DATE DEFAULT CURRENT_DATE
);


CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);


CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    doctor_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    department_id INT REFERENCES departments(department_id)
);


CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    appointment_date TIMESTAMP NOT NULL,
    appointment_status VARCHAR(30) DEFAULT 'Scheduled'
);


CREATE TABLE medical_records (
    record_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    diagnosis TEXT NOT NULL,
    treatment TEXT,
    record_date DATE DEFAULT CURRENT_DATE
);


CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(100),
    prescription_date DATE DEFAULT CURRENT_DATE
);

-- 2. SAMPLE DATA
INSERT INTO departments (department_name, location)
VALUES
('General Medicine', 'Freetown'),
('Paediatrics', 'Bo'),
('Cardiology', 'Kenema'),
('Surgery', 'Makeni');

INSERT INTO patients
(first_name, last_name, date_of_birth, gender, phone, address)
VALUES
('James', 'Kamara', '1990-05-12', 'Male', '076123456', 'Freetown'),
('Fatmata', 'Turay', '1985-08-20', 'Female', '077234567', 'Bo'),
('Mohamed', 'Bangura', '2000-03-15', 'Male', '078345678', 'Kenema'),
('Aminata', 'Conteh', '1995-11-25', 'Female', '076456789', 'Makeni'),
('Abdul', 'Sesay', '1978-02-10', 'Male', '077567890', 'Freetown');


SELECT * FROM patients;

SELECT * FROM departments;


INSERT INTO doctors (doctor_name, specialization, department_id)
VALUES
('Dr. John Williams', 'General Physician', 1),
('Dr. Sarah Johnson', 'Paediatrician', 2),
('Dr. Michael Brown', 'Cardiologist', 3),
('Dr. Mary Davis', 'Surgeon', 4);

SELECT * FROM doctors;
INSERT INTO appointments
(patient_id, doctor_id, appointment_date, appointment_status)
VALUES
(1, 1, '2026-11-10 09:00:00', 'Scheduled'),
(2, 2, '2026-11-10 10:30:00', 'Completed'),
(3, 3, '2026-11-11 11:00:00', 'Scheduled'),
(4, 4, '2026-11-12 14:00:00', 'Cancelled'),
(5, 1, '2026-11-13 08:30:00', 'Scheduled');


SELECT * FROM appointments;
INSERT INTO medical_records
(patient_id, doctor_id, diagnosis, treatment)
VALUES
(1, 1, 'Malaria', 'Prescribed appropriate treatment'),
(2, 2, 'Common Cold', 'Rest and supportive care'),
(3, 3, 'High Blood Pressure', 'Blood pressure monitoring'),
(4, 4, 'Minor Injury', 'Follow-up assessment'),
(5, 1, 'Routine Check-up', 'General health assessment');


INSERT INTO prescriptions
(patient_id, doctor_id, medication_name, dosage)
VALUES
(1, 1, 'Example Medication A', 'As prescribed'),
(2, 2, 'Example Medication B', 'As prescribed'),
(3, 3, 'Example Medication C', 'As prescribed'),
(4, 4, 'Example Medication D', 'As prescribed'),
(5, 1, 'Example Medication E', 'As prescribed');


SELECT
    patients.patient_id,
    patients.first_name,
    patients.last_name,
    doctors.doctor_name,
    appointments.appointment_date,
    appointments.appointment_status
FROM patients
INNER JOIN appointments
ON patients.patient_id = appointments.patient_id
INNER JOIN doctors
ON appointments.doctor_id = doctors.doctor_id;


SELECT
    patients.patient_id,
    patients.first_name,
    patients.last_name,
    appointments.appointment_date,
    appointments.appointment_status
FROM patients

-- 4. JOINS
LEFT JOIN appointments
ON patients.patient_id = appointments.patient_id;


SELECT
    patients.first_name,
    patients.last_name,
    appointments.appointment_id,
    appointments.appointment_date,
    appointments.appointment_status
FROM patients
RIGHT JOIN appointments
ON patients.patient_id = appointments.patient_id;

-- 5. VIEWS
CREATE VIEW patient_appointment_summary AS
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    d.doctor_name,
    a.appointment_date,
    a.appointment_status
FROM patients p
INNER JOIN appointments a
ON p.patient_id = a.patient_id
INNER JOIN doctors d
ON a.doctor_id = d.doctor_id;


-- 9. DATABASE INDEXES

CREATE INDEX IF NOT EXISTS idx_appointments_doctor_id
ON appointments(doctor_id);

CREATE INDEX IF NOT EXISTS idx_doctors_department_id
ON doctors(department_id);

CREATE INDEX IF NOT EXISTS idx_medical_records_patient_id
ON medical_records(patient_id);

CREATE INDEX IF NOT EXISTS idx_medical_records_doctor_id
ON medical_records(doctor_id);

CREATE INDEX IF NOT EXISTS idx_prescriptions_patient_id
ON prescriptions(patient_id);

CREATE INDEX IF NOT EXISTS idx_prescriptions_doctor_id
ON prescriptions(doctor_id);



SELECT * FROM patient_appointment_summary;
CREATE VIEW patient_medical_summary AS
SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    m.diagnosis,
    m.treatment,
    m.record_date,
    d.doctor_name
FROM patients p
INNER JOIN medical_records m
ON p.patient_id = m.patient_id
INNER JOIN doctors d
ON m.doctor_id = d.doctor_id;


SELECT * FROM patient_medical_summary;
CREATE TABLE medical_record_audit (
    audit_id SERIAL PRIMARY KEY,
    record_id INT,
    action_type VARCHAR(20),
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);


CREATE OR REPLACE FUNCTION audit_medical_records()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO medical_record_audit
    (record_id, action_type, description)
    VALUES
    (NEW.record_id, TG_OP, NEW.diagnosis);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER medical_record_audit_trigger
AFTER INSERT OR UPDATE
ON medical_records
FOR EACH ROW
EXECUTE FUNCTION audit_medical_records();


CREATE OR REPLACE FUNCTION update_appointment_status()
RETURNS TRIGGER AS $$
BEGIN
    NEW.appointment_status =
        COALESCE(NEW.appointment_status, 'Scheduled');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 7. TESTING
CREATE TRIGGER appointment_status_trigger
BEFORE INSERT OR UPDATE
ON appointments
FOR EACH ROW
EXECUTE FUNCTION update_appointment_status();


CREATE OR REPLACE PROCEDURE register_patient(
    p_first_name VARCHAR(50),
    p_last_name VARCHAR(50),
    p_date_of_birth DATE,
    p_gender VARCHAR(20),
    p_phone VARCHAR(20),
    p_address VARCHAR(150)
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO patients (
        first_name,
        last_name,
        date_of_birth,
        gender,
        phone,
        address
    )
    VALUES (
        p_first_name,
        p_last_name,
        p_date_of_birth,
        p_gender,
        p_phone,
        p_address
    );

    RAISE NOTICE 'Patient registered successfully.';
END;
$$;


CALL register_patient(
    'Ibrahim',
    'Koroma',
    '1992-06-15',
    'Male',
    '076987654',
    'Freetown'
);

-- 8. DISPLAYING RECORDS
SELECT * FROM patients
WHERE first_name = 'Ibrahim';


UPDATE medical_records
SET diagnosis = 'Malaria - Updated'
WHERE record_id = 1;


SELECT * FROM medical_record_audit;
INSERT INTO appointments
(patient_id, doctor_id, appointment_date)
VALUES
(6, 1, '2026-11-15 10:00:00');

SELECT * FROM appointments
WHERE patient_id = 6;

UPDATE medical_records
SET diagnosis = 'Malaria - Updated'
WHERE record_id = 1;

SELECT * FROM medical_records
WHERE record_id = 1;


SELECT * FROM medical_record_audit
ORDER BY audit_id DESC;


SELECT * FROM patient_medical_summary;


SELECT * FROM patient_appointment_summary;

SELECT * FROM prescriptions;

SELECT * FROM doctors;

SELECT * FROM departments;

SELECT * FROM appointments;

SELECT * FROM patients;


SELECT column_name
FROM information_schema.columns
WHERE table_name = 'appointments'
ORDER BY ordinal_position;

-- ADVANCED QUERY 1: Count total registered patients
SELECT COUNT(*) AS total_patients
FROM patients;

-- QUERY: Count appointments by status

SELECT
    appointment_status,
    COUNT(*) AS total_appointments
FROM appointments
GROUP BY appointment_status
ORDER BY total_appointments DESC;

-- ADVANCED QUERY 2: Count appointments for each doctor

SELECT
    d.doctor_name,
    COUNT(a.appointment_id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a
ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id, d.doctor_name
ORDER BY total_appointments DESC;

-- TRIGGER: Validate medical record diagnosis

CREATE OR REPLACE FUNCTION validate_medical_record_diagnosis()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.diagnosis IS NULL OR TRIM(NEW.diagnosis) = '' THEN
        RAISE EXCEPTION 'Diagnosis cannot be empty.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER medical_record_validate_diagnosis
BEFORE INSERT OR UPDATE
ON medical_records
FOR EACH ROW
EXECUTE FUNCTION validate_medical_record_diagnosis();



-- ADVANCED QUERY 5: Patients and their medical diagnoses

SELECT
    p.patient_id,
    p.first_name,
    p.last_name,
    m.diagnosis,
    m.treatment,
    m.record_date
FROM patients p
INNER JOIN medical_records m
ON p.patient_id = m.patient_id
ORDER BY m.record_date DESC;

-- ADVANCED QUERY 6: Doctors and their departments

SELECT
    d.doctor_name,
    d.specialization,
    dep.department_name,
    dep.location
FROM doctors d
INNER JOIN departments dep
ON d.department_id = dep.department_id
ORDER BY dep.department_name;


-- ADVANCED QUERY 7: Patients and their prescriptions

SELECT
    p.first_name,
    p.last_name,
    pr.medication_name,
    pr.dosage,
    pr.prescription_date
FROM patients p
INNER JOIN prescriptions pr
ON p.patient_id = pr.patient_id
ORDER BY pr.prescription_date DESC;



-- TRANSACTION TESTING

BEGIN;

INSERT INTO patients
(first_name, last_name, date_of_birth, gender, phone, address)
VALUES
('Transaction', 'Test', '2000-01-01', 'Male', '0700000000', 'Freetown');

ROLLBACK;
SELECT *
FROM patients
WHERE first_name = 'Transaction'
AND last_name = 'Test';


BEGIN;

INSERT INTO patients
(first_name, last_name, date_of_birth, gender, phone, address)
VALUES
('Commit', 'Test', '2001-02-15', 'Female', '0711111111', 'Freetown');

COMMIT;



SELECT *
FROM patients
WHERE first_name = 'Commit'
AND last_name = 'Test';


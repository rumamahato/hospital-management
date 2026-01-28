from django.db import models
from django.contrib.auth.models import User


# -------------------------
# Patient Profile
# -------------------------
class Patient(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    DOB = models.DateField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    )

    def __str__(self):
        return self.name

# -------------------------
# Doctor Profile
# -------------------------
class Doctor(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

# -------------------------
# Appointment
# -------------------------
class Appointment(models.Model):
    patient_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)

    doctor_name = models.CharField(max_length=150)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient_name} - {self.doctor_name}"



# -------------------------
# Medical Record
# -------------------------
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.SET_NULL,null=True,related_name='medical_records')
    doctor = models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='medical_records')
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor}"


# -------------------------
# Prescription
# -------------------------
class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.medicine_name


# -------------------------
# Payment
# -------------------------
class Payment(models.Model):
    patient = models.CharField(max_length=150)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('Esewa', 'Esewa'),
            ('Khalti', 'Khalti'),
            ('Card', 'Card'),
            ('Cash', 'Cash')
        ]
    )
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - Rs.{self.amount}"


# -------------------------
# Notification
# -------------------------
class Notification(models.Model):
    name = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class Payment(models.Model):

    PAYMENT_METHOD = (
        ('Cash', 'Cash'),
        ('Online', 'Online'),
        ('Card', 'Card'),
    )

    PAYMENT_STATUS = (
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    )

    medical_record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medical_record.patient.name} - Rs.{self.amount}"
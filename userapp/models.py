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

    # ✅ NEW: save the total amount entered in the form
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('Cash', 'Cash'),
            ('Esewa', 'Esewa'),
            ('Khalti', 'Khalti'),
            ('Card', 'Card'),
        ]
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
        ],
        default='Pending'
    )

    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.patient_name} - {self.status}"

class Notification(models.Model):
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
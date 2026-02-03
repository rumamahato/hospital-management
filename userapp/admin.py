from django.contrib import admin
from .models import (
    Patient,
    Doctor,
    Appointment,
    MedicalRecord,
    Prescription,
    Payment,
    Notification
)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'gender')
    search_fields = ('name', 'phone')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience', 'consultation_fee')
    list_filter = ('specialization',)
    search_fields = ('name', 'specialization')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name',
        'doctor_name',
        'appointment_date',
        'appointment_time',
        'status'
    )
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient_name', 'doctor_name')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')
    search_fields = ('patient__name', 'doctor__name')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'dosage', 'duration')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'amount',
        'payment_method',
        'status',
        'paid_on'
    )
    list_filter = ('payment_method', 'status')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_read', 'created_at')
    list_filter = ('is_read',)

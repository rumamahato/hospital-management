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
    list_display = ('patient_name', 'doctor_name', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__name', 'doctor__name')  # Use __ to search related fields


    # Methods to display names
    def patient_name(self, obj):
        return obj.patient.name
    patient_name.short_description = 'Patient Name'

    def doctor_name(self, obj):
        return obj.doctor.name
    doctor_name.short_description = 'Doctor Name'


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')
    search_fields = ('patient__name', 'doctor__name')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'dosage', 'duration')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Doctor, Patient, Appointment, MedicalRecord, Prescription
import uuid, hmac, hashlib, base64
from django.urls import reverse


# ---------------- Home & Auth ----------------
def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def index(request):
    if not request.user.is_staff:
        return redirect('login')

    context = {
        'd': Doctor.objects.count(),
        'p': Patient.objects.count(),
        'a': Appointment.objects.count(),
        'm': MedicalRecord.objects.count(),
        'pr': Prescription.objects.count(),
    }

    return render(request, 'index.html', context)

def login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(request, username=u, password=p)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error = "yes"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# ---------------- Doctor ----------------
def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    doc = Doctor.objects.filter(is_deleted=False)  # ✅ important

    if request.method == "POST":
        did = request.POST.get("doctor_id")
        doctor = get_object_or_404(Doctor, id=did, is_deleted=False)

        doctor.name = request.POST.get("name")
        doctor.specialization = request.POST.get("specialization")
        doctor.experience = request.POST.get("experience")
        doctor.available_from = request.POST.get("available_from")
        doctor.available_to = request.POST.get("available_to")
        doctor.consultation_fee = request.POST.get("consultation_fee")
        doctor.save()

        return redirect('view_doctor')

    return render(request, 'views_doctor.html', {'doc': doc})

def add_doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        try:
            Doctor.objects.create(
                name=request.POST['name'],
                contact=request.POST['contact'],  # <-- यहाँ contact field छ
                specialization=request.POST['special'],
                experience=request.POST['experience'],
                available_from=request.POST['available_from'],
                available_to=request.POST['available_to'],
                consultation_fee=request.POST['consultation_fee']
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'add_doctor.html', {'error': error})



def edit_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = get_object_or_404(Doctor, id=pid)
    error = ""
    if request.method == "POST":
        try:
            doctor.name = request.POST['name']
            doctor.contact = request.POST['contact']
            doctor.specialization = request.POST['special']
            doctor.experience = request.POST['experience']
            doctor.available_from = request.POST['available_from']
            doctor.available_to = request.POST['available_to']
            doctor.consultation_fee = request.POST['consultation_fee']
            doctor.save()
            error = "no"
            return redirect('view_doctor')
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'edit_doctor.html', {'doctor': doctor, 'error': error})

def delete_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')

    doctor = get_object_or_404(Doctor, id=pid)
    doctor.is_deleted = True        # ✅ recycle
    doctor.save()

    return redirect('recycle_doctor_view')

def recycle_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')

    doctor = get_object_or_404(Doctor, id=pid)
    doctor.is_deleted = True
    doctor.save()

    return redirect('view_doctor')

def recycle_bin_doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    doctors = Doctor.objects.filter(is_deleted=True)
    return render(request, 'recycle_doctor.html', {'doctors': doctors})

def restore_doctor(request, pid):
    doctor = get_object_or_404(Doctor, id=pid)
    doctor.is_deleted = False
    doctor.save()
    return redirect('recycle_bin_doctor')

def delete_doctor_permanent(request, pid):
    doctor = get_object_or_404(Doctor, id=pid)
    doctor.delete()
    return redirect('recycle_bin_doctor')



# ---------------- Patient ----------------
def view_patient(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        pid = request.POST.get("patient_id")
        patient = get_object_or_404(Patient, id=pid, is_deleted=False)

        patient.name = request.POST.get("name")
        patient.DOB = request.POST.get("DOB")
        patient.gender = request.POST.get("gender")
        patient.phone = request.POST.get("phone")
        patient.address = request.POST.get("address")
        patient.save()

        return redirect('view_patient')

    patients = Patient.objects.filter(is_deleted=False)
    return render(request, 'views_patient.html', {'patients': patients})


def add_patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        try:
            Patient.objects.create(
                name=request.POST['name'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                DOB=request.POST['dob'],
                gender=request.POST['gender'],
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'add_patient.html', {'error': error})

def edit_patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = get_object_or_404(Patient, id=pid)
    error = ""
    if request.method == "POST":
        try:
            patient.name = request.POST['name']
            patient.phone = request.POST['phone']
            patient.address = request.POST['address']
            patient.DOB = request.POST['dob']
            patient.gender = request.POST['gender']
            patient.save()
            error = "no"
            return redirect('view_patient')
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'edit_patient.html', {'patient': patient, 'error': error})

def delete_patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = get_object_or_404(Patient, id=pid)
    patient.delete()
    return redirect('view_patient')

def recycle_patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    
    patient = get_object_or_404(Patient, id=pid)
    patient.is_deleted = True
    patient.save()
    return redirect('view_patient')

def recycle_bin_patient(request):
    if not request.user.is_staff:
        return redirect('login')
    
    patients = Patient.objects.filter(is_deleted=True)
    return render(request, 'recycle_patient.html', {'patients': patients})

def restore_patient(request, pid):
    patient = get_object_or_404(Patient, id=pid)
    patient.is_deleted = False
    patient.save()
    return redirect('recycle_bin_patient')

def delete_patient_permanent(request, pid):
    patient = get_object_or_404(Patient, id=pid)
    patient.delete()
    return redirect('recycle_bin_patient')




# ---------------- Appointment ----------------
def add_appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    status_choices = Appointment._meta.get_field('status').choices  # 🔹 dynamically get choices
    error = None

    if request.method == "POST":
        try:
            patient = Patient.objects.get(id=request.POST['patient'])
            doctor = Doctor.objects.get(id=request.POST['doctor'])
            Appointment.objects.create(
                patient_name=patient.name,
                phone=patient.phone,
                gender=patient.gender,
                dob=patient.DOB,
                address=patient.address,
                doctor_name=doctor.name,
                appointment_date=request.POST['appointment_date'],
                appointment_time=request.POST['appointment_time'],
                status=request.POST['status']
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"

    return render(request, "add_appointment.html", {
        "patients": patients,
        "doctors": doctors,
        "status_choices": status_choices,
        "error": error
    })


def view_appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        appointment = get_object_or_404(
            Appointment,
            id=request.POST.get("appointment_id")
        )
        appointment.patient_name = request.POST.get("patient_name")
        appointment.doctor_name = request.POST.get("doctor_name")
        appointment.appointment_date = request.POST.get("appointment_date")
        appointment.appointment_time = request.POST.get("appointment_time")
        appointment.status = request.POST.get("status")
        appointment.save()
        return redirect('view_appointment')

    appointments = Appointment.objects.filter(is_deleted=False)
    return render(request, 'views_appointment.html', {'appointments': appointments})


def edit_appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=pid)
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    error = ""
    if request.method == "POST":
        try:
            patient_id = request.POST.get("patient")
            doctor_id = request.POST.get("doctor")
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)

            appointment.patient_name = patient.name
            appointment.phone = patient.phone
            appointment.gender = patient.gender
            appointment.dob = patient.DOB
            appointment.address = patient.address
            appointment.doctor_name = doctor.name
            appointment.appointment_date = request.POST.get("appointment_date")
            appointment.appointment_time = request.POST.get("appointment_time")
            appointment.status = request.POST.get("status")
            appointment.save()
            return redirect('view_appointment')
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, "edit_appointment.html", {"appointment": appointment, "patients": patients, "doctors": doctors, "error": error})

def delete_appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=pid)
    appointment.delete()
    return redirect('view_appointment')


def recycle_appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')

    appointment = get_object_or_404(Appointment, id=pid)
    appointment.is_deleted = True
    appointment.save()
    return redirect('view_appointment')

def recycle_bin_appointment(request):
    appointments = Appointment.objects.filter(is_deleted=True)
    return render(request, 'recycle_appointment.html', {'appointments': appointments})


def restore_appointment(request, pid):
    appointment = get_object_or_404(Appointment, id=pid)
    appointment.is_deleted = False
    appointment.save()
    return redirect('recycle_appointment_view')


def delete_appointment_permanent(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('recycle_bin_appointment')

def recycle_appointment_view(request):
    if not request.user.is_staff:
        return redirect('login')

    appointments = Appointment.objects.filter(is_deleted=True)
    return render(request, 'recycle_appointment.html', {'appointments': appointments})


def add_medical_record(request):
    if not request.user.is_staff:
        return redirect('login')

    error = ""

    patients = Patient.objects.filter(is_deleted=False)
    doctors = Doctor.objects.filter(is_deleted=False)

    if request.method == "POST":
        try:
            patient = Patient.objects.get(id=request.POST.get("patient"))
            doctor = Doctor.objects.get(id=request.POST.get("doctor"))

            MedicalRecord.objects.create(
                patient=patient,
                doctor=doctor,
                diagnosis=request.POST.get("diagnosis"),
                notes=request.POST.get("notes", "")
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"

    return render(request, 'add_medical_record.html', {
        'error': error,
        'patients': patients,
        'doctors': doctors
    })


def view_medical_record(request):
    if not request.user.is_staff:
        return redirect('login')

    records = MedicalRecord.objects.all()
    return render(request, 'views_medical_record.html', {'records': records})


def edit_medical_record(request, id):
    record = get_object_or_404(MedicalRecord, id=id)

    if request.method == "POST":
        record.diagnosis = request.POST.get("diagnosis")
        record.notes = request.POST.get("notes")
        record.save()
        return redirect('view_medical_record') 


def delete_medical_record(request, id):
    record = get_object_or_404(MedicalRecord, id=id)
    record.delete()
    return redirect('view_medical_record')  


# -------------------------
# Prescription
# -------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Doctor, Patient, Appointment, MedicalRecord, Prescription

# ---------------- Home & Auth ----------------
def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def index(request):
    if not request.user.is_staff:
        return redirect('login')

    context = {
        'd': Doctor.objects.count(),
        'p': Patient.objects.count(),
        'a': Appointment.objects.count(),
        'm': MedicalRecord.objects.count(),
        'pr': Prescription.objects.count(),
    }

    return render(request, 'index.html', context)

def login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(request, username=u, password=p)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            error = "yes"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# ---------------- Doctor ----------------
def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    doc = Doctor.objects.filter(is_deleted=False)  # ✅ important

    if request.method == "POST":
        did = request.POST.get("doctor_id")
        doctor = get_object_or_404(Doctor, id=did, is_deleted=False)

        doctor.name = request.POST.get("name")
        doctor.specialization = request.POST.get("specialization")
        doctor.experience = request.POST.get("experience")
        doctor.available_from = request.POST.get("available_from")
        doctor.available_to = request.POST.get("available_to")
        doctor.consultation_fee = request.POST.get("consultation_fee")
        doctor.save()

        return redirect('view_doctor')

    return render(request, 'views_doctor.html', {'doc': doc})

def add_doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        try:
            Doctor.objects.create(
                name=request.POST['name'],
                contact=request.POST['contact'],  # <-- यहाँ contact field छ
                specialization=request.POST['special'],
                experience=request.POST['experience'],
                available_from=request.POST['available_from'],
                available_to=request.POST['available_to'],
                consultation_fee=request.POST['consultation_fee']
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'add_doctor.html', {'error': error})



def edit_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = get_object_or_404(Doctor, id=pid)
    error = ""
    if request.method == "POST":
        try:
            doctor.name = request.POST['name']
            doctor.contact = request.POST['contact']
            doctor.specialization = request.POST['special']
            doctor.experience = request.POST['experience']
            doctor.available_from = request.POST['available_from']
            doctor.available_to = request.POST['available_to']
            doctor.consultation_fee = request.POST['consultation_fee']
            doctor.save()
            error = "no"
            return redirect('view_doctor')
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'edit_doctor.html', {'doctor': doctor, 'error': error})

def delete_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')

    doctor = get_object_or_404(Doctor, id=pid)
    doctor.is_deleted = True        # ✅ recycle
    doctor.save()

    return redirect('recycle_doctor_view')

def recycle_doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')

    doctor = get_object_or_404(Doctor, id=pid)
    doctor.is_deleted = True
    doctor.save()

    return redirect('view_doctor')

def recycle_bin_doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    doctors = Doctor.objects.filter(is_deleted=True)
    return render(request, 'recycle_doctor.html', {'doctors': doctors})

def restore_doctor(request, pid):
    doctor = get_object_or_404(Doctor, id=pid)
    doctor.is_deleted = False
    doctor.save()
    return redirect('recycle_bin_doctor')

def delete_doctor_permanent(request, pid):
    doctor = get_object_or_404(Doctor, id=pid)
    doctor.delete()
    return redirect('recycle_bin_doctor')



# ---------------- Patient ----------------
def view_patient(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        pid = request.POST.get("patient_id")
        patient = get_object_or_404(Patient, id=pid, is_deleted=False)

        patient.name = request.POST.get("name")
        patient.DOB = request.POST.get("DOB")
        patient.gender = request.POST.get("gender")
        patient.phone = request.POST.get("phone")
        patient.address = request.POST.get("address")
        patient.save()

        return redirect('view_patient')

    patients = Patient.objects.filter(is_deleted=False)
    return render(request, 'views_patient.html', {'patients': patients})


def add_patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == "POST":
        try:
            Patient.objects.create(
                name=request.POST['name'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                DOB=request.POST['dob'],
                gender=request.POST['gender'],
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'add_patient.html', {'error': error})

def edit_patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = get_object_or_404(Patient, id=pid)
    error = ""
    if request.method == "POST":
        try:
            patient.name = request.POST['name']
            patient.phone = request.POST['phone']
            patient.address = request.POST['address']
            patient.DOB = request.POST['dob']
            patient.gender = request.POST['gender']
            patient.save()
            error = "no"
            return redirect('view_patient')
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, 'edit_patient.html', {'patient': patient, 'error': error})

def delete_patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = get_object_or_404(Patient, id=pid)
    patient.delete()
    return redirect('view_patient')

def recycle_patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    
    patient = get_object_or_404(Patient, id=pid)
    patient.is_deleted = True
    patient.save()
    return redirect('view_patient')

def recycle_bin_patient(request):
    if not request.user.is_staff:
        return redirect('login')
    
    patients = Patient.objects.filter(is_deleted=True)
    return render(request, 'recycle_patient.html', {'patients': patients})

def restore_patient(request, pid):
    patient = get_object_or_404(Patient, id=pid)
    patient.is_deleted = False
    patient.save()
    return redirect('recycle_bin_patient')

def delete_patient_permanent(request, pid):
    patient = get_object_or_404(Patient, id=pid)
    patient.delete()
    return redirect('recycle_bin_patient')




# ---------------- Appointment ----------------
def add_appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    patients = Patient.objects.filter(is_deleted=False)
    doctors = Doctor.objects.filter(is_deleted=False)
    status_choices = Appointment._meta.get_field('status').choices
    error = None

    # 🔹 Default values (GET request)
    total_amount = 100
    tax_amount = 0

    if request.method == "POST":
        try:
            patient = Patient.objects.get(id=request.POST.get("patient"))
            doctor = Doctor.objects.get(id=request.POST.get("doctor"))

            # ✅ USER ENTERED AMOUNT
            total_amount = int(request.POST.get("total_amount", 0))

            appointment = Appointment.objects.create(
                patient_name=patient.name,
                phone=patient.phone,
                gender=patient.gender,
                dob=patient.DOB,
                address=patient.address,
                doctor_name=doctor.name,
                appointment_date=request.POST.get("appointment_date"),
                appointment_time=request.POST.get("appointment_time"),
                status=request.POST.get("status"),
                total_amount=total_amount   # ⭐ IMPORTANT
            )

            # payment success पछि status update गर्न
            request.session['appointment_id'] = appointment.id

            error = "no"

        except Exception as e:
            print(e)
            error = "yes"

    # ================= eSewa CONFIG =================
    transaction_uuid = str(uuid.uuid4())
    product_code = "EPAYTEST"
    signed_field_names = "total_amount,transaction_uuid,product_code"

    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret_key = "8gBm/:&EnhH.1/q"

    signature = base64.b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()

    success_url = request.build_absolute_uri(reverse("success_esewa"))
    failure_url = request.build_absolute_uri(reverse("failure_esewa"))

    return render(request, "add_appointment.html", {
        "patients": patients,
        "doctors": doctors,
        "status_choices": status_choices,
        "error": error,

        # ✅ eSewa dynamic values
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "transaction_uuid": transaction_uuid,
        "product_code": product_code,
        "signed_field_names": signed_field_names,
        "signature": signature,
        "success_url": success_url,
        "failure_url": failure_url,
    })


def view_appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        appointment = get_object_or_404(
            Appointment,
            id=request.POST.get("appointment_id")
        )
        appointment.patient_name = request.POST.get("patient_name")
        appointment.doctor_name = request.POST.get("doctor_name")
        appointment.appointment_date = request.POST.get("appointment_date")
        appointment.appointment_time = request.POST.get("appointment_time")
        appointment.status = request.POST.get("status")
        appointment.save()
        return redirect('view_appointment')
    appointments = Appointment.objects.filter(is_deleted=False)
    return render(request, 'views_appointment.html', {'appointments': appointments})


def edit_appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=pid)
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    error = ""
    if request.method == "POST":
        try:
            patient_id = request.POST.get("patient")
            doctor_id = request.POST.get("doctor")
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            appointment.patient_name = patient.name
            appointment.phone = patient.phone
            appointment.gender = patient.gender
            appointment.dob = patient.DOB
            appointment.address = patient.address
            appointment.doctor_name = doctor.name
            appointment.appointment_date = request.POST.get("appointment_date")
            appointment.appointment_time = request.POST.get("appointment_time")
            appointment.status = request.POST.get("status")
            appointment.save()
            return redirect('view_appointment')
        except Exception as e:
            print(e)
            error = "yes"
    return render(request, "edit_appointment.html", {"appointment": appointment, "patients": patients, "doctors": doctors, "error": error})

def delete_appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=pid)
    appointment.delete()
    return redirect('view_appointment')


def recycle_appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')

    appointment = get_object_or_404(Appointment, id=pid)
    appointment.is_deleted = True
    appointment.save()
    return redirect('view_appointment')

def recycle_bin_appointment(request):
    appointments = Appointment.objects.filter(is_deleted=True)
    return render(request, 'recycle_appointment.html', {'appointments': appointments})


def restore_appointment(request, pid):
    appointment = get_object_or_404(Appointment, id=pid)
    appointment.is_deleted = False
    appointment.save()
    return redirect('recycle_appointment_view')


def delete_appointment_permanent(request, pid):
    appointment = get_object_or_404(Appointment, id=pid)
    appointment.delete()
    return redirect('recycle_appointment_view')

def recycle_appointment_view(request):
    if not request.user.is_staff:
        return redirect('login')

    appointments = Appointment.objects.filter(is_deleted=True)
    return render(request, 'recycle_appointment.html', {'appointments': appointments})


def add_medical_record(request):
    if not request.user.is_staff:
        return redirect('login')

    error = ""

    patients = Patient.objects.filter(is_deleted=False)
    doctors = Doctor.objects.filter(is_deleted=False)

    if request.method == "POST":
        try:
            patient = Patient.objects.get(id=request.POST.get("patient"))
            doctor = Doctor.objects.get(id=request.POST.get("doctor"))

            MedicalRecord.objects.create(
                patient=patient,
                doctor=doctor,
                diagnosis=request.POST.get("diagnosis"),
                notes=request.POST.get("notes", "")
            )
            error = "no"
        except Exception as e:
            print(e)
            error = "yes"

    return render(request, 'add_medical_record.html', {
        'error': error,
        'patients': patients,
        'doctors': doctors
    })


def view_medical_record(request):
    if not request.user.is_staff:
        return redirect('login')

    records = MedicalRecord.objects.all()
    return render(request, 'views_medical_record.html', {'records': records})


def edit_medical_record(request, id):
    record = get_object_or_404(MedicalRecord, id=id)

    if request.method == "POST":
        record.diagnosis = request.POST.get("diagnosis")
        record.notes = request.POST.get("notes")
        record.save()
        return redirect('view_medical_record') 


def delete_medical_record(request, id):
    record = get_object_or_404(MedicalRecord, id=id)
    record.delete()
    return redirect('view_medical_record')  


# -------------------------
# Prescription
# -------------------------
def add_prescription(request):
    records = MedicalRecord.objects.all()
    error = ""

    if request.method == "POST":
        try:
            record_id = request.POST.get("medical_record")
            record = get_object_or_404(MedicalRecord, id=record_id)
            Prescription.objects.create(
                medical_record=record,
                medicine_name=request.POST.get("medicine_name"),
                dosage=request.POST.get("dosage"),
                duration=request.POST.get("duration"),
                instructions=request.POST.get("instructions")
            )
            return redirect('view_medical_record', id=record.id)
        except Exception as e:
            print(e)
            error = "yes"

    return render(request, 'add_prescription.html', {'records': records, 'error': error})


def view_prescription(request, id):
    medical_record = get_object_or_404(MedicalRecord, id=id)
    prescriptions = Prescription.objects.filter(medical_record=medical_record)

    return render(request, 'views_prescription.html', {
        'medical_record': medical_record,
        'prescriptions': prescriptions,
    })


def payment_success(request):
    appointment_id = request.session.get('appointment_id')

    if appointment_id:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = "Confirmed"
        appointment.save()
        del request.session['appointment_id']

    return render(request, "payment_success.html")

def payment_failure(request):
    return render(request, "payment_failure.html")
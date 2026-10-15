from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
import random
from datetime import date
from django.db.models import Q


def landing_view(req):
    doctors = Doctor.objects.all()
    total_doctors = doctors.count()
    total_appointments = DoctorAppointment.objects.count()
    
    context = {
        'doctors': doctors,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
    }
    return render(req, 'landing.html', context)




def booking_appoinment_view(req):
    doctors = Doctor.objects.all()
    slots = TimeSlot.objects.all()
    today_date = date.today().strftime('%Y-%m-%d')

    if req.method == 'POST':
        name = req.POST.get('name', '').strip()
        phone = req.POST.get('phone', '').strip()
        city = req.POST.get('city', '').strip()
        age = req.POST.get('age', 18)
        apt_date = req.POST.get('date')
        doctor_id = req.POST.get('doctor')
        slot_id = req.POST.get('time_slot')

        try:
            selected_doctor = Doctor.objects.get(id=doctor_id)
            selected_slot = TimeSlot.objects.get(id=slot_id)

            # Check: Double booking roko
            is_busy = DoctorAppointment.objects.filter(
                doctor=selected_doctor,
                appointment_date=apt_date,
                time_slot=selected_slot,
                status='Confirmed'
            ).exists()

            if is_busy:
                messages.error(req, f"Dr. {selected_doctor.name} iss slot ({selected_slot.slot}) par pehle se booked hain. Kripya koi doosra slot ya date chunein.")
                return render(req, 'book.html', {'doctors': doctors, 'slots': slots, 'today': today_date})

            # Random Unique Reference ID
            unique_id = f"DOC-{random.randint(100000, 999999)}"

            DoctorAppointment.objects.create(
                booking_id=unique_id,
                patient_name=name,
                patient_phone=phone,
                patient_city=city,
                patient_age=age,
                doctor=selected_doctor,
                time_slot=selected_slot,
                appointment_date=apt_date,
                status='Confirmed'
            )

            messages.success(req, f"Appointment successfully book ho gaya! Aapki Booking ID hai: {unique_id}")
            return redirect('show_all')

        except Exception as e:
            messages.error(req, f"Booking fail ho gayi: {e}")

    context = {
        'doctors': doctors,
        'slots': slots,
        'today': today_date
    }
    return render(req, 'book.html', context)










def show_all_view(req):
   # 1. Base QuerySet (select_related optimize karke N+1 queries roki)
    appointments = DoctorAppointment.objects.select_related('doctor', 'time_slot').all().order_by('-id')

    # 2. Reception Metrics / Stat Badges
    total_confirmed = appointments.filter(status='Confirmed').count()
    total_cancelled = appointments.filter(status='Cancelled').count()
    total_doctors = Doctor.objects.count()

    # 3. Form se GET parameters read karein
    search_query = req.GET.get('search', '').strip()
    status_filter = req.GET.get('status', '').strip()
    doctor_filter = req.GET.get('doctor', '').strip()

    # 4. Search Filter (Name, Phone, Booking ID)
    if search_query:
        appointments = appointments.filter(
            Q(patient_name__icontains=search_query) |
            Q(patient_phone__icontains=search_query) |
            Q(booking_id__icontains=search_query)
        )

    # 5. Status Filter
    if status_filter and status_filter != 'All':
        appointments = appointments.filter(status=status_filter)

    # 6. Doctor Filter
    if doctor_filter and doctor_filter != 'All':
        appointments = appointments.filter(doctor_id=doctor_filter)

    doctors = Doctor.objects.all()

    context = {
        'booking': appointments,
        'doctors': doctors,
        'search_query': search_query,
        'status_filter': status_filter,
        'doctor_filter': doctor_filter,
        'total_confirmed': total_confirmed,
        'total_cancelled': total_cancelled,
        'total_doctors': total_doctors,
    }
    return render(req, 'show.html', context)


def cancel_booking_view(req,booking_id):
    appointment = get_object_or_404(
        DoctorAppointment.objects.select_related('doctor', 'time_slot'), 
        booking_id=booking_id
    )

    # Agar pehle se cancelled hai
    if appointment.status == 'Cancelled':
        messages.warning(req, f"Booking {booking_id} pehle se cancelled hai!")
        return redirect('show_all')

    if req.method == 'POST':
        reason = req.POST.get('reason', '').strip()
        if not reason:
            messages.error(req, "Kripya cancellation ka reason zaroor batayein!")
            return render(req, 'cancel_app.html', {'appoinment': appointment})

        # Soft Delete update
        appointment.status = 'Cancelled'
        appointment.cancellation_reason = reason
        appointment.save()

        messages.success(req, f"Booking ID {booking_id} successfully cancel kar di gayi hai.")
        return redirect('show_all')

    return render(req, 'cancel_app.html', {'appoinment': appointment})
from django.contrib import admin
from .models import Doctor, TimeSlot, DoctorAppointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'fee')
    search_fields = ('name', 'specialization')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot')

@admin.register(DoctorAppointment)
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'patient_name', 'doctor', 'appointment_date', 'time_slot', 'status')
    list_filter = ('status', 'doctor', 'appointment_date')
    search_fields = ('booking_id', 'patient_name', 'patient_phone')
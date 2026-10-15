from django.db import models

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.0)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization} (₹{self.fee})"

class TimeSlot(models.Model):
    slot = models.CharField(max_length=50)

    def __str__(self):
        return self.slot


class DoctorAppointment(models.Model):
    booking_id = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=15)
    patient_city = models.CharField(max_length=100)
    patient_age = models.IntegerField(default=18)

   
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    status = models.CharField(max_length=20, default='Confirmed')
    cancellation_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.booking_id} - {self.patient_name} (Dr. {self.doctor.name})"
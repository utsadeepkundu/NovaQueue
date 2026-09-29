# core/models.py
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

from django.db import models
from django.contrib.auth.models import User
# core/models.py

class Queue(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 1. Add a default or allow blank for existing rows
    symptoms = models.TextField(default="") 
    
    # 2. Urgency score already has a default, so it's fine
    urgency_score = models.FloatField(default=0.0)
    
    # 3. For token_number, if you have existing rows, 'unique=True' will crash 
    # if you give them all the same default. 
    # Best for dev: allow null temporarily or clear the table.
    token_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    doctor_notes = models.TextField(blank=True, null=True)
    
    arrival_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    estimated_wait_time = models.IntegerField(default=0)
    room_number = models.CharField(max_length=50, blank=True, null=True)
    is_checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    ai_prescription = models.TextField(null=True, blank=True) 

    class Meta:
        ordering = ['arrival_time']


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor_name = models.CharField(max_length=100, default="Dr. Smith") # Can be a ForeignKey to a Doctor model later
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    doctor_notes = models.TextField(blank=True, null=True)
    ai_prescription = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.username} - {self.appointment_date} at {self.appointment_time}"
from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    medical_condition = models.TextField()
    medication_regimen = models.TextField()
    allergies = models.TextField()
    last_appointment = models.DateTimeField()
    next_appointment = models.DateTimeField()
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class chatSessions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class chatMessages(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(chatSessions, on_delete=models.CASCADE)
    message = models.TextField()
    time_sent = models.DateTimeField(auto_now_add=True)

    SENDER_CHOICES = (
        ('User', 'User'),
        ('Bot', 'Agent'),
    )
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)

    def __str__(self):
        return self.message
# Generated by Django 4.2.16 on 2024-10-26 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='chatSessions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('medical_condition', models.TextField()),
                ('medication_regimen', models.TextField()),
                ('allergies', models.TextField()),
                ('last_appointment', models.DateTimeField()),
                ('next_appointment', models.DateTimeField()),
                ('doctor_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='chatMessages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('sender', models.CharField(choices=[('User', 'User'), ('Bot', 'Agent')], max_length=4)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.chatsessions')),
            ],
        ),
    ]

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import *



from .ai_engine import MedicalAIEngine
from django.utils import timezone


@login_required
def request_token(request):
    # Check if patient already has an active token (Waiting or In-Progress)
    existing_token = Queue.objects.filter(
        patient=request.user, 
        status__in=['waiting', 'in-progress']
    ).first()
    
    if existing_token:
        messages.warning(request, "You already have an active token.")
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form = TokenRequestForm(request.POST)
        if form.is_valid():
            token = form.save(commit=False)
            token.patient = request.user
            
            # AI Logic: Analyze symptoms
            symptoms = form.cleaned_data['symptoms']
            token.urgency_score = MedicalAIEngine.analyze_urgency(symptoms)
            
            # FIX: Count ALL tokens created today to avoid IntegrityError (Unique constraint)
            # Instead of counting only 'waiting', we count everything created today.
            today = timezone.now().date()
            total_tokens_today = Queue.objects.filter(arrival_time__date=today).count()
            
            # Calculate position for wait time (only those still waiting)
            waiting_count = Queue.objects.filter(status='waiting').count()
            token.estimated_wait_time = MedicalAIEngine.predict_wait_time(waiting_count, token.urgency_score)
            
            # Generate Unique Token Number
            date_str = today.strftime('%Y%m%d')
            token.token_number = f"T-{date_str}-{total_tokens_today + 1}"
            
            token.save()
            messages.success(request, f"Token {token.token_number} generated successfully!")
            return redirect('patient_dashboard')
    else:
        form = TokenRequestForm()
    
    return render(request, 'patient/request_token.html', {'form': form})

def home(request):
    return render(request, 'public/home.html')

def about(request):
    return render(request, 'public/about.html')

def contact(request):
    return render(request, 'public/contact.html')

def signup_patient(request):
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        profile_form = PatientProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, f"Account created for {user.username}! You can now login.")
            return redirect('login')
    else:
        user_form = PatientUserForm()
        profile_form = PatientProfileForm()
    
    return render(request, 'public/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

from django.contrib.auth.decorators import login_required

@login_required
def patient_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    
    # Find the active token for this user
    active_token = Queue.objects.filter(
        patient=request.user, 
        status__in=['waiting', 'in-progress']
    ).first()
    
    return render(request, 'patient/dashboard.html', {
        'active_token': active_token
    })

# Update login_success view if you want custom logic after login
def login_success(request):
    """
    Optional: Redirect users based on role after login.
    Configure this in settings.py: LOGIN_REDIRECT_URL = 'login_success'
    """
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('patient_dashboard')
    

@staff_member_required
def admin_dashboard(request):
    total_patients = User.objects.filter(is_superuser=False).count()
    active_queues = Queue.objects.filter(status='waiting').count()
    avg_wait = "14 mins" 
    
    # Fetch the 5 most recent activities based on arrival time
    recent_activities = Queue.objects.all().order_by('-arrival_time')[:5]
    
    context = {
        'total_patients': total_patients,
        'active_queues': active_queues,
        'avg_wait': avg_wait,
        'recent_activities': recent_activities,
    }
    return render(request, 'admin/dashboard.html', context)
from django.contrib.auth import logout
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')
@staff_member_required
def patient_list(request):
    patients = User.objects.filter(is_superuser=False).select_related('profile')
    return render(request, 'admin/patient_list.html', {'patients': patients})

@staff_member_required
def patient_create(request):
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        profile_form = PatientProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Patient created successfully.")
            return redirect('manage_patients')
    else:
        user_form = PatientUserForm()
        profile_form = PatientProfileForm()
    return render(request, 'admin/patient_form.html', {'user_form': user_form, 'profile_form': profile_form, 'title': 'Add Patient'})

@staff_member_required
def patient_update(request, pk):
    patient_user = get_object_or_404(User, pk=pk)
    # Ensure profile exists
    profile, created = PatientProfile.objects.get_or_create(user=patient_user)
    
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST, instance=patient_user)
        profile_form = PatientProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Patient updated successfully.")
            return redirect('manage_patients')
    else:
        user_form = PatientUserForm(instance=patient_user)
        # Note: We exclude password for updates in a real scenario, 
        # but using the same form for simplicity here.
        profile_form = PatientProfileForm(instance=profile)
        
    return render(request, 'admin/patient_form.html', {'user_form': user_form, 'profile_form': profile_form, 'title': 'Edit Patient'})

@staff_member_required
def patient_delete(request, pk):
    patient = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Patient deleted.")
        return redirect('manage_patients')
    return render(request, 'admin/patient_confirm_delete.html', {'patient': patient})

# --- HELPER: Aggressive Dynamic Priority Logic ---
def get_optimized_queue():
    """
    Fetches the waiting list and applies the Time-Based Priority Boost.
    Formula: Final Score = AI Score + (1 point per minute waiting > 30 mins)
    """
    waiting_list = list(Queue.objects.filter(status='waiting'))
    now = timezone.now()
    
    for item in waiting_list:
        # 1. Calculate Wait Time in Minutes
        wait_seconds = (now - item.arrival_time).total_seconds()
        wait_mins = int(wait_seconds / 60)
        item.wait_mins_display = wait_mins 
        
        # 2. Calculate Boost (Aggressive: 1 point per minute overdue)
        boost_score = 0.0
        if wait_mins > 30:
            overdue_mins = wait_mins - 30
            # LOGIC: 1 point boost for every 1 min overdue
            boost_score = float(overdue_mins) 
        
        # 3. Calculate Final Dynamic Score
        raw_score = item.urgency_score + boost_score
        
        # Cap standard patients at 9.9 so they don't overtake 'Code Red' (10.0)
        if item.urgency_score < 10.0:
            item.dynamic_score = min(round(raw_score, 1), 9.9)
        else:
            item.dynamic_score = 10.0 # Keep Code Red at max
            
        item.boost_amount = round(boost_score, 1)

    # 4. Sort: Highest Score first, then Earliest Arrival
    waiting_list.sort(key=lambda x: (x.dynamic_score, x.arrival_time.timestamp() * -1), reverse=True)
    
    return waiting_list

@staff_member_required
def manage_queue(request):
    waiting_list = get_optimized_queue()
    active_patient = Queue.objects.filter(status='in-progress').first()
    completed_list = Queue.objects.filter(status='completed').order_by('-arrival_time')[:5]
    
    patients = User.objects.filter(is_superuser=False).order_by('first_name')

    return render(request, 'admin/manage_queue.html', {
        'waiting_list': waiting_list,
        'waiting_count': len(waiting_list),
        'active_patient': active_patient,
        'completed_list': completed_list,
        'patients': patients  # Pass patients to template
    })
@staff_member_required
def generate_offline_token(request):
    """
    Admin generates a token for a walk-in patient. 
    Automatically marks them as checked-in since they are at the hospital.
    """
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        symptoms = request.POST.get('symptoms')
        
        if not patient_id or not symptoms:
            messages.error(request, "Patient and symptoms are required.")
            return redirect('manage_queue')
            
        patient = get_object_or_404(User, id=patient_id)
        
        # Check if they already have an active token
        if Queue.objects.filter(patient=patient, status__in=['waiting', 'in-progress']).exists():
            messages.error(request, f"{patient.first_name} already has an active token in the queue.")
            return redirect('manage_queue')
            
        # AI Logic
        urgency_score = MedicalAIEngine.analyze_urgency(symptoms)
        
        today = timezone.now().date()
        total_tokens_today = Queue.objects.filter(arrival_time__date=today).count()
        waiting_count = Queue.objects.filter(status='waiting').count()
        wait_time = MedicalAIEngine.predict_wait_time(waiting_count, urgency_score)
        
        token_number = f"T-{today.strftime('%Y%m%d')}-{total_tokens_today + 1}"
        
        # Create and Auto-Check-in
        Queue.objects.create(
            patient=patient,
            token_number=token_number,
            symptoms=symptoms,
            urgency_score=urgency_score,
            estimated_wait_time=wait_time,
            is_checked_in=True,           # AUTO CHECK-IN
            check_in_time=timezone.now()  # SET CHECK-IN TIME
        )
        messages.success(request, f"Walk-in Token {token_number} created & checked-in for {patient.first_name}.")
        
    return redirect('manage_queue')
@staff_member_required
def call_next_patient(request):
    """
    Picks the next patient based on Dynamic Score (Urgency + Wait Time).
    """
    if Queue.objects.filter(status='in-progress').exists():
        messages.error(request, "A patient is already being treated.")
        return redirect('manage_queue')

    # UPDATED: Get the sorted list to pick the correct person
    optimized_queue = get_optimized_queue()
    
    if optimized_queue:
        next_patient = optimized_queue[0] # Pick the top scored patient
        
        room_no = request.POST.get('room_number', 'Room 1')
        next_patient.status = 'in-progress'
        next_patient.room_number = room_no
        next_patient.save()
        
        # SMS Notification (Optional, remove if you don't have utils.py set up)
        try:
            from .utils import send_hospital_sms
            patient_phone = next_patient.patient.profile.phone
            msg = f"NovaQueue: It's your turn! Please proceed to {room_no}."
            send_hospital_sms(patient_phone, msg)
        except:
            pass 
            
        messages.success(request, f"Called {next_patient.patient.get_full_name()} to {room_no}")
    else:
        messages.info(request, "No patients in waiting list.")
        
    return redirect('manage_queue')

@staff_member_required
def update_queue_status(request, pk, new_status):
    token = get_object_or_404(Queue, pk=pk)
    token.status = new_status
    token.save()
    messages.success(request, f"Patient {token.token_number} marked as {new_status}")
    return redirect('manage_queue')


@login_required
def my_tokens(request):
    """
    Displays active tokens (Waiting or In-Progress) for the current patient.
    """
    tokens = Queue.objects.filter(
        patient=request.user, 
        status__in=['waiting', 'in-progress']
    ).order_by('-arrival_time')
    return render(request, 'patient/my_tokens.html', {'tokens': tokens})

@login_required
def patient_history(request):
    """
    Displays past tokens (Completed or Skipped) for the current patient.
    """
    tokens = Queue.objects.filter(
        patient=request.user, 
        status__in=['completed', 'skipped']
    ).order_by('-arrival_time')
    return render(request, 'patient/history.html', {'tokens': tokens})
@login_required
def profile_settings(request):
    if request.method == 'POST':
        # Simple update logic
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')
            
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile_settings')

    return render(request, 'patient/profile_settings.html')

# core/views.py
from .ai_prescriptions import generate_ai_prescription

@staff_member_required
def complete_session(request, pk):
    token = get_object_or_404(Queue, pk=pk)
    if request.method == 'POST':
        notes = request.POST.get('doctor_notes')
        token.doctor_notes = notes
        token.status = 'completed'
        
        # Trigger the AI Assistant
        if notes:
            token.ai_prescription = generate_ai_prescription(notes)
            
        token.save()
        return redirect('manage_queue')

@staff_member_required
def admin_history(request):
    """
    Global history view for administrators to see all processed tokens.
    """
    # Fetch all completed or skipped tokens, most recent first
    history_tokens = Queue.objects.filter(
        status__in=['completed', 'skipped']
    ).select_related('patient', 'patient__profile').order_by('-arrival_time')
    
    return render(request, 'admin/history.html', {
        'history_tokens': history_tokens
    })


@staff_member_required
def history_edit(request, pk):
    """
    Allows admin to modify a past visit record (symptoms, notes, or status).
    """
    token = get_object_or_404(Queue, pk=pk)
    if request.method == 'POST':
        token.symptoms = request.POST.get('symptoms')
        token.doctor_notes = request.POST.get('doctor_notes')
        token.status = request.POST.get('status')
        token.save()
        messages.success(request, f"Record {token.token_number} updated successfully.")
        return redirect('admin_history')
    
    return render(request, 'admin/history_edit.html', {'token': token})

@staff_member_required
def history_delete(request, pk):
    """
    Permanently removes a history record from the database.
    """
    token = get_object_or_404(Queue, pk=pk)
    if request.method == 'POST':
        token_id = token.token_number
        token.delete()
        messages.success(request, f"Record {token_id} has been permanently deleted.")
        return redirect('admin_history')
    
    return render(request, 'admin/history_confirm_delete.html', {'token': token})


from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@staff_member_required
def qr_scanner(request):
    """View to render the camera-based QR scanner for admins."""
    return render(request, 'admin/scanner.html')

@csrf_exempt
@staff_member_required
def process_check_in(request):
    """API endpoint called by the scanner to check-in a patient."""
    if request.method == 'POST':
        data = json.loads(request.body)
        token_no = data.get('token_number')
        
        try:
            token = Queue.objects.get(token_number=token_no, status='waiting')
            if not token.is_checked_in:
                token.is_checked_in = True
                token.check_in_time = timezone.now()
                token.save()
                return JsonResponse({
                    'status': 'success', 
                    'message': f'Checked in: {token.patient.get_full_name()}',
                    'patient': token.patient.get_full_name()
                })
            else:
                return JsonResponse({'status': 'info', 'message': 'Patient already checked in.'})
        except Queue.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

import datetime

@login_required
def book_appointment(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        reason = request.POST.get('reason')
        doctor = request.POST.get('doctor', 'Dr. Smith')
        
        # Simple validation
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj < datetime.date.today():
                messages.error(request, "Cannot book appointments in the past.")
                return redirect('book_appointment')
                
            # Check for conflict (Simple logic: 1 appointment per slot per doctor)
            conflict = Appointment.objects.filter(
                doctor_name=doctor, 
                appointment_date=date_str, 
                appointment_time=time_str,
                status='scheduled'
            ).exists()
            
            if conflict:
                messages.error(request, "This time slot is already booked. Please choose another.")
                return redirect('book_appointment')
            
            Appointment.objects.create(
                patient=request.user,
                doctor_name=doctor,
                appointment_date=date_str,
                appointment_time=time_str,
                reason=reason
            )
            messages.success(request, "Appointment booked successfully!")
            return redirect('my_appointments')
            
        except ValueError:
            messages.error(request, "Invalid date or time format.")
    
    # Generate next 7 days dates
    today = datetime.date.today()
    dates = [(today + datetime.timedelta(days=i)) for i in range(8)]
    
    # Generate time slots (9 AM to 5 PM)
    times = [
        datetime.time(hour=h, minute=0) for h in range(9, 17)
    ]
    
    return render(request, 'patient/book_appointment.html', {
        'dates': dates, 
        'times': times
    })

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-appointment_date')
    return render(request, 'patient/my_appointments.html', {'appointments': appointments})

@staff_member_required
def admin_appointments(request):
    # Fetch today's appointments by default
    today = datetime.date.today()
    # Optional: Filter by date from GET param
    filter_date = request.GET.get('date', str(today))
    
    appointments = Appointment.objects.filter(appointment_date=filter_date).order_by('appointment_time')
    
    return render(request, 'admin/manage_appointments.html', {
        'appointments': appointments,
        'filter_date': filter_date
    })

@staff_member_required
def complete_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        notes = request.POST.get('doctor_notes')
        appt.doctor_notes = notes
        appt.status = 'completed'
        
        # Reuse AI Logic for Appointments too!
        if notes:
            appt.ai_prescription = generate_ai_prescription(notes)
            
        appt.save()
        messages.success(request, "Appointment completed and prescription generated.")
        return redirect('admin_appointments')
    return redirect('admin_appointments')

from .analytics import get_analytics_data
import json

@staff_member_required
def admin_analytics(request):
    data = get_analytics_data()
    
    # Convert data to JSON for use in JavaScript
    context = {
        'analytics_data': json.dumps(data)
    }
    return render(request, 'admin/analytics.html', context)
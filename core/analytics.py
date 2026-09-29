from django.db.models import Count, Avg
from django.db.models.functions import ExtractHour
from .models import Queue, Appointment
import json

def get_analytics_data():
    """
    Aggregates data for the admin dashboard charts.
    """
    
    # 1. Status Distribution (Pie Chart)
    status_counts = Queue.objects.values('status').annotate(count=Count('status'))
    status_data = {item['status']: item['count'] for item in status_counts}
    
    # 2. Urgency Distribution (Bar Chart)
    # Group urgency scores into ranges: Low (1-4), Medium (5-7), High (8-9), Critical (10)
    urgency_data = {
        'Low': Queue.objects.filter(urgency_score__lt=5).count(),
        'Medium': Queue.objects.filter(urgency_score__gte=5, urgency_score__lt=8).count(),
        'High': Queue.objects.filter(urgency_score__gte=8, urgency_score__lt=10).count(),
        'Critical': Queue.objects.filter(urgency_score__gte=10).count(),
    }

    # 3. Peak Hours (Line Chart)
    # Extract hour from arrival_time and count tokens per hour
    peak_hours = Queue.objects.annotate(hour=ExtractHour('arrival_time')).values('hour').annotate(count=Count('id')).order_by('hour')
    
    # Initialize all hours 0-23 with 0 count
    hourly_counts = {h: 0 for h in range(24)}
    for entry in peak_hours:
        if entry['hour'] is not None:
            hourly_counts[entry['hour']] = entry['count']
            
    return {
        'status_labels': list(status_data.keys()),
        'status_values': list(status_data.values()),
        'urgency_labels': list(urgency_data.keys()),
        'urgency_values': list(urgency_data.values()),
        'peak_hours_labels': [f"{h}:00" for h in range(24)],
        'peak_hours_values': list(hourly_counts.values()),
    }
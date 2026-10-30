from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Application


@shared_task
def send_interview_reminders(hours_ahead=24):
    """Email users about interviews happening in the next `hours_ahead` hours (runs hourly via beat)."""
    now = timezone.now()
    due = Application.objects.filter(
        status=Application.Status.INTERVIEW,
        reminder_sent=False,
        interview_at__gt=now,
        interview_at__lte=now + timedelta(hours=hours_ahead),
    ).select_related("user")

    sent = 0
    for app in due:
        when = timezone.localtime(app.interview_at).strftime("%d %b %Y, %I:%M %p")
        send_mail(
            subject=f"Interview reminder: {app.role} at {app.company}",
            message=(
                f"Hi {app.user.first_name or 'there'},\n\n"
                f"Your interview for {app.role} at {app.company} is on {when}.\n"
                "All the best!\n\n- Job Tracker"
            ),
            from_email=None,
            recipient_list=[app.user.email],
        )
        app.reminder_sent = True
        app.save(update_fields=["reminder_sent"])
        sent += 1
    return sent

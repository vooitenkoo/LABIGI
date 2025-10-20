from django.utils import timezone
from datetime import datetime
import calendar
import pytz

def timezone_info(request):
    user_timezone = request.session.get('user_timezone', 'UTC')
    if user_timezone not in pytz.all_timezones:
        user_timezone = 'UTC'
    
    user_tz = pytz.timezone(user_timezone)
    utc_now = timezone.now()
    user_now = utc_now.astimezone(user_tz)
    
    cal = calendar.TextCalendar(calendar.MONDAY)
    current_calendar = cal.formatmonth(user_now.year, user_now.month)
    
    return {
        'user_timezone': user_timezone,
        'utc_now': utc_now.strftime('%d/%m/%Y %H:%M:%S'),
        'user_now': user_now.strftime('%d/%m/%Y %H:%M:%S'),
        'current_calendar': current_calendar,
    } 
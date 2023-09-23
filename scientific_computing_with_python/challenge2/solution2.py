def convert_time_to_minutes(time):
    """Converts a time in format '00:00' or '00:00 AM' into a number of minutes"""

    time_components = time.split()
    (hours, minutes) = [int(elem) for elem in time_components[0].split(':')]

    if len(time_components) == 2 and time_components[1] == "PM" and hours != 12:
        hours += 12
    if len(time_components) == 2 and time_components[1] == "AM" and hours == 12:
        hours = 0

    return hours * 60 + minutes


def convert_minutes_to_time(minutes, weekday):
    """Converts a number of minutes into a time string in the format '00:00 AM' with the extra text '(N days later)' if necessary, 
    and adds a day of the week if the weekday argument is supplied"""

    WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    am_pm = "AM" if hours < 12 else "PM"

    if hours > 12:
        hours -= 12
    elif hours == 0:
        hours = 12

    minutes_remainder = minutes % 60
    minutes_prefix = '0' if len(str(minutes_remainder)) == 1 else ''

    weekday_text = ''
    if weekday:
       for i in range(len(WEEKDAYS)):
           if weekday.lower() == WEEKDAYS[i].lower():
               weekday_text = ", " + WEEKDAYS[(i + days) % 7]

    next_day_text = '' if not days else " (next day)" if days == 1 else f' ({days} days later)'

    return f'{hours}:{minutes_prefix}{minutes_remainder} {am_pm}{weekday_text}{next_day_text}'

def add_time(start, duration, weekday=False):
    """Uses a helper function to convert start and duration to minutes, adds them together and uses another helper to format the result as a time string"""

    time_in_minutes = convert_time_to_minutes(start) + convert_time_to_minutes(duration)

    return convert_minutes_to_time(time_in_minutes, weekday)

import pytz
import sqlite3
import pyttsx3
import re
import speech_recognition as sr
from datetime import datetime, timedelta
import pyaudio

recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('volume', 0.9)

conn = sqlite3.connect('smart_speaker_ehie.db')
c = conn.cursor()

c.execute('''
        CREATE TABLE IF NOT EXISTS alarms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alarm_time TEXT NOT NULL
        )
    ''')


def recognise_speech():
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="en-US")
            print("You said:", text)
            engine.say("You said: " + text)
            engine.runAndWait()
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand what you said")
            engine.say("Sorry, could not understand what you said")
            engine.runAndWait()
            return ""


number_dictionary = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
    "twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24, "twenty-five": 25,
    "twenty-six": 26, "twenty-seven": 27, "twenty-eight": 28, "twenty-nine": 29, "thirty": 30,
    "thirty-one": 31, "thirty-two": 32, "thirty-three": 33, "thirty-four": 34, "thirty-five": 35,
    "thirty-six": 36, "thirty-seven": 37, "thirty-eight": 38, "thirty-nine": 39, "forty": 40,
    "forty-one": 41, "forty-two": 42, "forty-three": 43, "forty-four": 44, "forty-five": 45,
    "forty-six": 46, "forty-seven": 47, "forty-eight": 48, "forty-nine": 49, "fifty": 50,
    "fifty-one": 51, "fifty-two": 52, "fifty-three": 53, "fifty-four": 54, "fifty-five": 55,
    "fifty-six": 56, "fifty-seven": 57, "fifty-eight": 58, "fifty-nine": 59, "sixty": 60
}


def adjust_hour_based_on_context(hour, context):
    pm_indicators = {'pm', 'afternoon', 'evening', 'night'}  # Set of keywords indicating PM
    context_words = set(context.lower().split())  # Normalize and split context into words

    if context_words & pm_indicators:  # Check for intersection
        if hour == 12:
            adjusted_hour = 12  # If it's 12 PM, it should stay 12
        elif hour < 12:
            adjusted_hour = hour + 12  # Convert AM hour to PM by adding 12
        else:
            adjusted_hour = hour  # Keep hour as is if it's already in PM format
        return adjusted_hour

    return hour  # Return original hour if no PM indicator is found


def calculate_alarm_time(hour, minute, context, current_time):
    hour = adjust_hour_based_on_context(hour, context)

    alarm_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)

    if alarm_time <= current_time:
        alarm_time += timedelta(days=1)

    return alarm_time


def parse_minute_and_adjust_hour(full_match, position, hour):
    if position == 'past':
        minute = int(full_match) if full_match.isdigit() else number_dictionary.get(full_match.lower(), 0)
    elif position == 'to':
        minute = 60 - (int(full_match) if full_match.isdigit() else number_dictionary.get(full_match.lower(), 0))
        hour = (hour - 1) % 24  # Adjust hour backward
    else:
        minute = 30 if 'half' in full_match else 0  # Default to 0 if unrecognized pattern
    return minute, hour


def parse_time(text):
    current_time = datetime.now(pytz.timezone('GMT'))
    words = text.split()
    words = [str(number_dictionary.get(word.lower(), word)) for word in words]
    text = ' '.join(words)

    pattern = re.compile(
        r'\b((half|quarter|\d+)\s(past|to))\s(\d{1,2})\s*(in the\s|at\s)?(afternoon|night|evening|tonight)?',
        re.IGNORECASE)

    matches = pattern.findall(text)

    times = []

    for full_match, minute_word, position, hour, _, context in matches:
        hour = int(hour)
        minute, adjusted_hour = parse_minute_and_adjust_hour(minute_word, position, hour)
        alarm_time = calculate_alarm_time(adjusted_hour, minute, context, current_time)
        times.append(alarm_time.strftime('%H:%M'))

    return times


def add_alarm(alarm_time):
    c.execute("INSERT INTO alarms (alarm_time) VALUES (?)", (alarm_time,))

    conn.commit()


def remove_alarm(alarm_time):
    c.execute("DELETE FROM alarms WHERE alarm_time = ?", (alarm_time,))

    conn.commit()


def get_alarms():
    c.execute("SELECT alarm_time FROM alarms")  # Query to select all 'alarm_id' from the 'alarms' table
    rows = c.fetchall()

    if rows:
        # Create a message that includes all alarm IDs separated by ' an alarm '
        alarms = [row[0] for row in rows]
        if len(alarms) > 1:
            # Join all but the last alarm with ', ', and add 'and' before the last alarm
            alarm_list = ', '.join(alarms[:-1]) + ', and, ' + alarms[-1]
        else:
            alarm_list = alarms[0]  # Only one alarm, so no need for commas or 'and'

        message = f"You have alarms set for {alarm_list}."
    else:
        message = "You have no alarms set."

    engine.say(message)
    engine.runAndWait()


def main():
    while True:
        text = recognise_speech()
        if "add alarm" in text:
            alarm_time = parse_time(text)
            add_alarm(alarm_time)
            engine.say("alarm added")
            engine.runAndWait()
            break
        elif "remove alarm" in text:
            remove_alarm(parse_time(text))
            engine.say(f"alarm for {parse_time(text)} removed")
            engine.runAndWait()
            break
        elif "get alarms" in text:
            get_alarms()
            break


if __name__ == "__main__":
    main()

conn.close()

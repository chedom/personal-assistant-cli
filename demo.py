import subprocess
import sys
import time
import random
import threading
from datetime import datetime, timedelta

PAUSED = False


def human_type(proc, text):
    """Prints command by symbol, as human"""
    for ch in text:
        while PAUSED:
            time.sleep(0.1)
        proc.stdin.write(ch)
        proc.stdin.flush()
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(random.uniform(0.02, 0.08))
    proc.stdin.write("\n")
    proc.stdin.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()
    time.sleep(1)  # wait for next


def pause_listener():
    """Listen SPACE key to pause resume"""
    global PAUSED
    try:
        import msvcrt  # Windows
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    PAUSED = not PAUSED
                    print("[DEMO PAUSED]" if PAUSED else "[DEMO RESUMED]")
            time.sleep(0.1)
    except ImportError:
        import sys
        import termios
        import tty
        import select  # Unix
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
        try:
            while True:
                dr, dw, de = select.select([sys.stdin], [], [], 0)
                if dr:
                    ch = sys.stdin.read(1)
                    if ch == ' ':
                        PAUSED = not PAUSED
                        print("[DEMO PAUSED]" if PAUSED else "[DEMO RESUMED]")
                time.sleep(0.1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    proc = subprocess.Popen(
        ["python", "-u", "main.py", "--demo"],  # unbuffered
        stdin=subprocess.PIPE,
        stdout=None,  # output to current console
        stderr=None,
        text=True
    )
    listener = threading.Thread(target=pause_listener, daemon=True)
    listener.start()

    time.sleep(2)

    # ----------------------
    # General
    # ----------------------
    human_type(proc, "hello")

    # Helper to format birthdays in the past
    def past_birthday(years_ago):
        birth_date = datetime.now() - timedelta(days=years_ago * 365)
        return birth_date.strftime("%d.%m.%Y")

    def random_phone():
        """
        Generate a random Ukrainian phone number in format +380 XX XXX XXXX
        where XX is the operator code.
        """
        #
        operator_codes = [
            "50", "67", "68", "73", "91", "92",
            "93", "94", "95", "96", "97", "98", "99"
        ]

        operator = random.choice(operator_codes)
        number = random.randint(1000000, 9999999)
        return f"+380{operator}{number}"

    # ----------------------
    # Contacts (3 contacts with phone numbers)
    # ----------------------
    contacts = [
        ("Olena", random_phone(), 25, "12 Shevchenko St, Kyiv, Ukraine"),
        ("Ivan", random_phone(), 30, ""),
        ("Max", random_phone(), 50, "")
    ]

    for idx, (name, phone, years, address) in enumerate(contacts):
        human_type(proc, f"add {name} {phone}")
        human_type(proc, f"set-birthday {name} {past_birthday(years)}")
        if idx == 0:
            human_type(proc, f"set-email {name} {name.lower()}@example.com")
            human_type(proc, f"set-address {name} \"{address}\"")
            new_phone = random_phone()
            human_type(proc, f"add {name} {new_phone}")
            human_type(proc, f"phone {name}")
            human_type(proc, f"change {name} {new_phone} {random_phone()}")

    human_type(proc, "all")
    human_type(proc, "find olena")
    human_type(proc, "find *van")
    human_type(proc, "find *Shevchenko*")

    human_type(proc, f"delete-phone {contacts[0][0]} {contacts[0][1]}")
    human_type(proc, "delete-email Ivan")
    human_type(proc, "set-email Ivan incorrect-email")
    human_type(proc, "delete-birthday Max")
    human_type(proc, "delete-address Olena")

    # ----------------------
    # Upcoming birthdays (e.g., in 7 days)
    # ----------------------
    human_type(proc, "birthdays 7")

    human_type(proc, "delete-contact Olena")
    human_type(proc, "all")

    # ----------------------
    # Notes (realistic titles, descriptions, and tags)
    # ----------------------
    notes = [
        ("Meeting with team", "Discuss project milestones", "work,team,important"),
        ("Grocery shopping", "Buy milk, eggs, bread", "personal,shopping"),
        ("Doctor appointment", "Annual check-up at clinic", "health,important")
    ]

    for idx, (title, body, tags) in enumerate(notes, start=1):
        human_type(proc, f'add-note "{title}" "{body}" {tags}')
        if idx == 1:
            human_type(proc, f"note {idx}")
            human_type(proc, f"edit-note-title {idx} {title} (updated)")
            human_type(proc, f"edit-note-body {idx} {body} (updated)")
            human_type(proc, f"edit-note-tags {idx} {tags + ',updated'}")

    human_type(proc, "find-notes milk")
    human_type(proc, "find-notes-tags personal,work")
    human_type(proc, "sort-notes-tags health,important")

    human_type(proc, "delete-note 1")
    human_type(proc, "notes")

    human_type(proc, "exit")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

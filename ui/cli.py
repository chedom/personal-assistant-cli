import math
from storage.contacts_storage import ContactsStorage
from repositories.contacts import ContactsRepository
from services.contacts_service import ContactsService

from services import NotesService
from ui.factory import create_notes_repo

from core.app_context import AppContext
from ui.commands import handle_command


def welcome_message():
    header_width = 110
    divider = "-" * header_width
    border_width = 1
    message = 'WELCOME TO THE PERSONAL ASSISTANT TOOL!'
    space = (header_width - len(message) - (border_width * 2)) / 2
    print(divider, f"\n|{' ' * math.floor(space)}{message}{' ' * math.ceil(space)}|", f"\n{divider}")


def main():
    notes_repository = create_notes_repo("notes.json")

    ctx = AppContext(
        ContactsService(ContactsRepository(ContactsStorage())),
        NotesService(notes_repository, notes_repository)
    )

    welcome_message()
    handle_command('help', ctx)

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue
            result = handle_command(user_input, ctx)
            if result == "exit":
                break
            if result:
                print(result)
        except KeyboardInterrupt:
            handle_command("exit", ctx)
            break

    notes_repository.flush()


if __name__ == "__main__":
    main()

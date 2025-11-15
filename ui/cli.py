import math
from services.contacts_service import ContactsService

from ui.output_util import Out

from services import NotesService
from ui.factory import create_notes_repo, create_contacts_repo, SerializerType

from core.app_context import AppContext
from ui.commands import handle_command

try:
    # Support arrows, command history on unix systems
    import readline  # noqa: F401
except ImportError:
    pass


def welcome_message():
    header_width = 110
    divider = "-" * header_width
    border_width = 1
    message = 'WELCOME TO THE PERSONAL ASSISTANT TOOL!'
    space = (header_width - len(message) - (border_width * 2)) / 2
    print(
        divider,
        f"\n|{' ' * math.floor(space)}{Out.section(message)}{' ' * math.ceil(space)}|",
        f"\n{Out.section(divider)}{Out.RESET}"
    )


def main():
    contacts_repository = create_contacts_repo("contacts", SerializerType.PICKLE)
    notes_repository = create_notes_repo("notes", SerializerType.PICKLE)

    ctx = AppContext(
        ContactsService(contacts_repository),
        NotesService(notes_repository, notes_repository)
    )

    welcome_message()
    print(handle_command('help', ctx))

    while True:
        try:
            user_input = input(Out.input_prompt("Enter a command: ")).strip()
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
    contacts_repository.flush()


if __name__ == "__main__":
    main()

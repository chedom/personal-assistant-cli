import math
import sys

from services.contacts_service import ContactsService
from ui.output_util import Out
from services import NotesService
from ui.factory import create_notes_repo, create_contacts_repo, SerializerType
from core.app_context import AppContext
from ui.commands import handle_command, get_available_commands


def welcome_message():
    """Print a stylized welcome message to the user."""
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


def init_autocomplete(available_commands: list):
    """
    Initialize command-line autocomplete for available commands.
    """
    try:
        # Support arrows, command history on unix systems and cmd autocomplete
        import readline  # noqa: F401
    except ImportError:
        return

    def completer(text, state):
        buf = readline.get_line_buffer()
        end = readline.get_endidx()
        if " " in buf[:end]:
            return None

        options = [c for c in available_commands if c.startswith(text)]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind('set completion-ignore-case on')

    # Handle tab completion based on readline implementation
    # Check if using libedit (macOS) or GNU readline (Linux)
    if readline.__doc__ and 'libedit' in readline.__doc__:
        # macOS libedit syntax
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        # GNU readline syntax (Linux)
        readline.parse_and_bind("tab: complete")


def main():
    init_autocomplete(get_available_commands())

    is_demo = "--demo" in sys.argv
    storage_dir = "demo/" if is_demo else ""

    contacts_repository = create_contacts_repo(
        f"{storage_dir}contacts",
        SerializerType.PICKLE
    )
    notes_repository = create_notes_repo(
        f"{storage_dir}notes",
        SerializerType.PICKLE
    )

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

    if not is_demo:
        notes_repository.flush()
        contacts_repository.flush()


if __name__ == "__main__":
    main()

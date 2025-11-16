from colorama import Fore, Style, init
from models.contact import Contact
from models.note import Note

init(autoreset=True)


class Out:
    """
    Utility class for consistent colored CLI output.

    Provides static methods to format messages with color and style,
    including errors, warnings, success messages, info, logging, commands,
    sections, input prompts, contacts, and notes.
    """
    # -------- COLOR STYLES -------- #
    ERROR = Fore.RED + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    VALID = Fore.MAGENTA + Style.BRIGHT
    INFO = Fore.CYAN
    LOG = Fore.LIGHTBLACK_EX
    COMMAND = Fore.BLUE + Style.BRIGHT
    PARAM = Fore.YELLOW
    SECTION = Fore.WHITE + Style.BRIGHT
    INPUT = Fore.GREEN + Style.BRIGHT
    RESET = Style.RESET_ALL

    # -------- ERROR -------- #
    @staticmethod
    def error(msg: str) -> str:
        """Return a formatted error message."""
        return f"{Out.ERROR}Error: {msg}{Out.RESET}"

    # -------- SUCCESS -------- #
    @staticmethod
    def success(msg: str) -> str:
        """Return a formatted success message."""
        return f"{Out.SUCCESS}{msg}{Out.RESET}"

    # -------- WARNING -------- #
    @staticmethod
    def warn(msg: str) -> str:
        """Return a formatted warning message."""
        return f"{Out.WARNING}Warning: {msg}{Out.RESET}"

    # -------- VALIDATION MESSAGES -------- #
    @staticmethod
    def validation(msg: str) -> str:
        """Return a formatted validation message."""
        return f"{Out.VALID}Validation: {msg}{Out.RESET}"

    # -------- LOG / SYSTEM OUTPUT -------- #
    @staticmethod
    def log(msg: str) -> str:
        """Return a formatted log message."""
        return f"{Out.LOG}[LOG] {msg}{Out.RESET}"

    # -------- COMMAND HELP -------- #
    @staticmethod
    def cmd(name: str, params: str = "") -> str:
        """Return a formatted command string with optional parameters."""
        if params:
            return f"{Out.COMMAND}{name} {Out.PARAM}{params}{Out.RESET}"
        return f"{Out.COMMAND}{name}{Out.RESET}"

    @staticmethod
    def section(title: str) -> str:
        """Return a formatted section header string."""
        return f"{Out.SECTION}{title}{Out.RESET}"

    # -------- CLI INPUT PROMPT -------- #
    @staticmethod
    def input_prompt(text: str) -> str:
        """Return a formatted input prompt string."""
        return f"{Out.INPUT}{text}{Out.RESET}"

    @staticmethod
    def res_attribute(text: str) -> str:
        """Return a formatted string for highlighting result attributes."""
        return f"{Out.INFO}{text}{Out.RESET}"

    @staticmethod
    def contact(contact: Contact) -> str:
        """Return a formatted multi-line string representing a Contact object."""
        phones_str = f"{Out.RESET} | {Out.INFO}".join(
            p.value for p in contact.phones
        ) or "—"
        parts = [
            f"{Out.SECTION}Contact:{Out.RESET} "
            f"{Out.INFO}{contact.name.value}{Out.RESET}",
            f"{Out.PARAM} > Phones: {Out.INFO}{phones_str}{Out.RESET}"
        ]

        if contact.email:
            parts.append(f"{Out.PARAM} > Email: {Out.INFO}{contact.email}{Out.RESET}")
        if contact.birthday:
            parts.append(
                f"{Out.PARAM} > Birthday: {Out.INFO}{contact.birthday}{Out.RESET}"
            )
        if contact.address:
            parts.append(
                f"{Out.PARAM} > Address: {Out.INFO}{contact.address}{Out.RESET}"
            )

        return "\n".join(parts)

    @staticmethod
    def note(note: Note):
        """Return a formatted multi-line string representing a Note object."""
        tags_str = ",".join([str(t) for t in note.tags]) if note.tags else "—"
        return (
            f"{Out.SECTION}Note:{Out.RESET}\n"
            f"{Out.PARAM} > ID: {Out.INFO}{note.note_id}{Out.RESET}\n"
            f"{Out.PARAM} > Title: {Out.INFO}{note.title}{Out.RESET}\n"
            f"{Out.PARAM} > Body: {Out.INFO}{note.body}{Out.RESET}\n"
            f"{Out.PARAM} > Tags: {Out.INFO}{tags_str}{Out.RESET}\n"
            f"{Out.PARAM} > Created at: "
            f"{Out.INFO}{note.created_at:%d.%m.%Y}{Out.RESET}\n"
            f"{Out.PARAM} > Updated at: "
            f"{Out.INFO}{note.updated_at:%d.%m.%Y}{Out.RESET}"
        )

    @staticmethod
    def note_preview(note: Note):
        """Return a shortened preview string for a Note object."""
        tags_str = ",".join([v.value for v in note.tags]) if note.tags else "—"
        return (
            f"{Out.SECTION}Note #{note.note_id} ({note.updated_at:%d.%m.%Y}): "
            f"{Out.INFO}{note.field_preview(note.title)}\n"
            f"{Out.PARAM}Body: {Out.INFO}{note.field_preview(note.body)}\n"
            f"{Out.PARAM}Tags: {Out.INFO}{tags_str}\n"
        )

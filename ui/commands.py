import shlex
from typing import Dict, List, Tuple, Callable
from core.app_context import AppContext

from ui.error_util import input_error
from ui.output_util import Out

from services import (
    CreateNoteReq,
    GetNoteReq,
    EditTitleReq,
    EditBodyReq,
    EditTagsReq,
    FindReq,
    FindByTagsReq,
    SortByTagsReq,
    DeleteReq,
)


# ---------- CONTACT COMMANDS ----------

def add_contact(args, ctx: AppContext):
    """Add a new contact or add phone to an existing contact."""
    if len(args) < 2:
        raise ValueError("add command requires 2 arguments: username and phone")

    name = args[0]
    phone = " ".join(args[1:])

    res = ctx.contacts.add_contact_or_phone(name, phone)
    return {
        "contact": f"Contact {Out.res_attribute(name)} was added to the book.",
        "phone": f"Phone was added to the contact {Out.res_attribute(name)}."
    }.get(res, '')


def set_email(args, ctx: AppContext):
    """Set email for a contact."""
    if len(args) < 2:
        raise ValueError(
            "set-email command requires 2 arguments: username and email"
        )

    name, email, *_ = args
    ctx.contacts.set_email(name, email)
    return "Email was set for the contact."


def set_birthday(args, ctx: AppContext):
    """Set birthday for a contact."""
    if len(args) < 2:
        raise ValueError(
            "set-birthday command requires 2 arguments: username and birthday"
        )

    name, birthday, *_ = args
    ctx.contacts.set_birthday(name, birthday)
    return "Birthday has been set for the contact."


def show_birthday(args, ctx: AppContext):
    """Show birthday of a contact."""
    if len(args) < 1:
        raise ValueError(
            "show-birthday command requires 1 arguments: username"
        )

    username = args[0]
    contact = ctx.contacts.get(username)
    if contact.birthday is None:
        return 'Birthday is not set for this contact yet.'

    return contact.birthday.value


def set_address(args, ctx: AppContext):
    """Set address for a contact."""
    if len(args) < 2:
        raise ValueError(
            "set-address command requires 2 arguments: username and address"
        )

    username = args[0]
    address = " ".join(args[1:])
    ctx.contacts.set_address(username, address)
    return "Address was set for the contact."


def edit_phone(args, ctx: AppContext):
    """Edit an existing phone number of a contact."""
    if len(args) < 3:
        raise ValueError(
            "edit command requires 3 arguments: username prev phone number and new phone"
        )

    username, prev_phone, new_phone, *_ = args
    ctx.contacts.edit_phone(username, prev_phone, new_phone)
    return "Contact’s phone was successfully changed."


def delete_email(args, ctx: AppContext):
    """Remove email from a contact."""
    if len(args) < 1:
        raise ValueError(
            "delete email command requires 1 arguments: username"
        )

    username = args[0]
    ctx.contacts.set_email(username, None)
    return f"Email was removed from {Out.res_attribute(username)}."


def delete_birthday(args, ctx: AppContext):
    """Remove birthday from a contact."""
    if len(args) < 1:
        raise ValueError(
            "delete birthday command requires 1 arguments: username"
        )

    username = args[0]
    ctx.contacts.set_birthday(username, None)
    return f"Birthday was removed from {Out.res_attribute(username)}."


def delete_address(args, ctx: AppContext):
    """Remove address from a contact."""
    if len(args) < 1:
        raise ValueError(
            "delete address command requires 1 arguments: username"
        )

    username = args[0]
    ctx.contacts.set_address(username, None)
    return f"Address was removed from {Out.res_attribute(username)}."


def find_contacts(args, ctx: AppContext):
    """Find contacts by name, phone, email, birthday, or address."""
    if not args:
        raise ValueError("Find command requires a search_text argument")

    search = " ".join(args)
    contacts = ctx.contacts.find(search)

    if not contacts:
        return f"No contact name, phone, email or birthday found for this search text: {Out.res_attribute(search)}"

    lines = [Out.section("> FOUND CONTACTS <")]
    for contact in contacts:
        lines.append(Out.contact(contact))

    return "\n\n".join(lines)


def all_contacts(args, ctx: AppContext):
    """List all contacts in the contact book."""
    contacts = ctx.contacts.all()

    if not contacts:
        return Out.warn("No contacts found in the book.")

    lines = [Out.section("> ALL CONTACTS <")]
    for contact in contacts:
        lines.append(Out.contact(contact))
    return "\n\n".join(lines)


def get_contact_phones(args, ctx: AppContext):
    """Get all phone numbers of a contact."""
    if len(args) < 1:
        raise ValueError(
            "get contact command requires 1 arguments: username"
        )

    username = args[0]
    contact = ctx.contacts.get(username)
    return f'{Out.PARAM}Phone: {Out.INFO}' + f'{Out.RESET}, {Out.INFO}'.join(
        [p.value for p in contact.phones]) + f"{Out.RESET}"


def upcoming_birthdays(args, ctx: AppContext):
    """List upcoming birthdays in a given number of days."""
    if not args:
        raise ValueError("Command requires number of days as argument")

    try:
        num_days = int(args[0])
    except ValueError:
        raise ValueError("Number of days must be an integer")

    contacts = ctx.contacts.upcoming_birthdays(num_days)

    if not contacts:
        return Out.warn(f"No upcoming birthdays in the book for closest [{num_days}] days")

    lines = [f"Upcoming birthdays for closest [{Out.res_attribute(str(num_days))}] days:"]
    for contact, next_birthday in contacts:
        lines.append(f"{Out.PARAM}{contact.name.value}: {Out.INFO}{next_birthday.strftime('%d.%m.%Y')}{Out.RESET}")
    return "\n".join(lines)


def delete_phone(args, ctx: AppContext):
    """Delete a phone number from a contact."""
    if len(args) < 2:
        raise ValueError("delete-phone command requires 2 arguments: username and phone")

    name = args[0]
    phone = " ".join(args[1:])
    ctx.contacts.del_phone(name, phone)
    return f"Phone was removed from {Out.res_attribute(name)}."


def delete_contact(args, ctx: AppContext):
    """Delete a contact by name."""
    if len(args) < 1:
        raise ValueError("delete-contact command requires 1 argument: username")

    ctx.contacts.del_contact(args[0])
    return f"Contact {Out.res_attribute(args[0])} deleted successfully"


# ---------- NOTE COMMANDS ----------
def _get_note_id(note_id: str):
    """Convert note_id string to integer and validate."""
    try:
        return int(note_id)
    except ValueError:
        raise ValueError('Note ID must be an integer')


def add_note(args, ctx: AppContext):
    """Add a new note with title, body, and tags."""
    if len(args) < 3:
        raise ValueError("add note command requires 3 argument: title body tags")

    title, body, tags, *_ = args
    req = CreateNoteReq(
        title=title,
        body=body.replace(r"\n", "\n"),  # allow new line symbol
        tags=tags.split(","),
    )
    note = ctx.notes.add_note(req)

    return Out.note(note)


def get_note(args, ctx: AppContext):
    """Retrieve a note by its ID."""
    if len(args) < 1:
        raise ValueError("get note command requires 1 argument: note_id")

    note_id = _get_note_id(args[0])
    req = GetNoteReq(note_id=note_id)
    note = ctx.notes.get_note(req)

    return Out.note(note)


def edit_note_title(args, ctx: AppContext):
    """Edit the title of a note."""
    if len(args) < 2:
        raise ValueError("edit note title command requires 2 argument: note_id title")

    note_id = _get_note_id(args[0])
    title = ' '.join(args[1:])
    req = EditTitleReq(note_id=note_id, title=title)
    note = ctx.notes.edit_title(req)

    return Out.note(note)


def edit_note_body(args, ctx: AppContext):
    """Edit the body of a note."""
    if len(args) < 2:
        raise ValueError("edit note body command requires 2 argument: note_id body")

    note_id = _get_note_id(args[0])
    body = ' '.join(args[1:])

    req = EditBodyReq(note_id=note_id, body=body.replace(r"\n", "\n"))
    note = ctx.notes.edit_body(req)

    return Out.note(note)


def edit_note_tags(args, ctx: AppContext):
    """Edit the tags of a note."""
    if len(args) < 2:
        raise ValueError("edit note tags command requires 2 argument: note_id tags")

    note_id = _get_note_id(args[0])
    tags = ','.join(args[1:])

    req = EditTagsReq(note_id=int(note_id), tags=tags.split(","), )
    note = ctx.notes.edit_tags(req)

    return Out.note(note)


def find_notes(args, ctx: AppContext):
    """Find notes by text query."""
    if len(args) < 1:
        raise ValueError("find notes command requires 1 argument: query")

    query = ' '.join(args)

    req = FindReq(query=query)
    notes = ctx.notes.find(req)

    return '\n'.join([Out.note_preview(n) for n in notes])


def find_notes_by_tags(args, ctx: AppContext):
    """Find notes matching specific tags."""
    if len(args) < 1:
        raise ValueError("find notes by tags command requires 1 argument: tags")

    tags = ','.join(args)
    req = FindByTagsReq(tags=tags.split(","))
    notes = ctx.notes.find_by_tags(req)

    return '\n'.join([Out.note_preview(n) for n in notes])


def sort_notes_by_tags(args, ctx: AppContext):
    """Sort notes by number of matching tags."""
    if len(args) < 1:
        raise ValueError("sort notes by tag command requires 1 argument: tags")

    tags = ','.join(args)
    req = SortByTagsReq(tags=tags.split(","))
    notes = ctx.notes.sort_by_tags(req)

    return '\n'.join([Out.note_preview(n) for n in notes])


def delete_note(args, ctx: AppContext):
    """Delete a note by its ID."""
    if len(args) < 1:
        raise ValueError("delete note command requires 1 argument: tags")

    note_id = _get_note_id(args[0])
    ctx.notes.delete_note(DeleteReq(note_id=note_id))

    return f"Note {Out.res_attribute(str(note_id))} has been successfully deleted"


def all_notes(args, ctx: AppContext):
    """List all notes."""
    notes = ctx.notes.all()

    return '\n'.join([Out.note_preview(n) for n in notes])


# ---------- SYSTEM COMMANDS ----------


# flake8: noqa: E501
def help_command(args, ctx: AppContext):
    """Return a help string listing all available commands."""
    def section(title: str) -> str:
        return Out.section(title)

    general = [
        (("hello",), "Show greeting"),
        (("help",), "Show possible commands"),
        (("close / exit",), "Exit the bot"),
    ]

    contacts = [
        (("add", "<username> <phone>"), "Add new contact or add phone to existing one"),
        (("change", "<username> <old_phone> <new_phone>"), "Update contact's phone"),
        (("phone", "<username>"), "Show contact's phone number(s)"),
        (("all",), "Show all contacts"),
        (("find", "<search_text>"), "Find matching contacts; supports * wildcard"),
        (("set-birthday", "<username> <DD.MM.YYYY>"), "Set contact's birthday"),
        (("show-birthday", "<username>"), "Show contact's birthday"),
        (("birthdays", "<days>"), "Show upcoming birthdays in N days"),
        (("set-email", "<username> <email>"), "Set email for contact"),
        (("set-address", "<username> <address>"), "Set address for contact"),
        (("delete-phone", "<username> <phone>"), "Delete phone from contact"),
        (("delete-email", "<username>"), "Delete contact's email"),
        (("delete-birthday", "<username>"), "Delete contact's birthday"),
        (("delete-address", "<username>"), "Delete contact's address"),
        (("delete-contact", "<username>"), "Delete contact"),
    ]

    notes = [
        (("add-note", "<note>"), "Add note, returns created note"),
        (("note", "<note-id>"), "Show note details"),
        (("notes",), "Show all notes"),
        (("edit-note-title", "<note-id> <new-title>"), "Change note's title"),
        (("edit-note-body", "<note-id> <new-body>"), "Change note's body"),
        (("edit-note-tags", "<note-id> <tags>"), "Change note's tags (comma separated)"),
        (("find-notes", "<query>"), "Find notes by text in title/body"),
        (("find-notes-tags", "<tags>"), "Find notes by tags"),
        (("sort-notes-tags", "<tags>"), "Sort notes by tags"),
        (("delete-note", "<note-id>"), "Delete note"),
    ]

    def render_block(title: str, commands: list[tuple[tuple[str, ...], str]]):
        lines = [section(title)]
        for (cmd_name, *cmd_args), description in commands:
            args_str = cmd_args[0] if cmd_args else ""
            lines.append(f"  {Out.cmd(cmd_name, args_str)} - {description}")
        return lines

    output = []
    output += [section("Available commands:"), ""]
    output += render_block("# General commands", general)
    output += [""]
    output += render_block("# Contact's commands", contacts)
    output += [""]
    output += render_block("# Note's commands", notes)

    return "\n".join(output)


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    """Parse user input into command and argument list."""
    args = shlex.split(user_input)
    if not args:
        return "", []
    command = args[0].lower()
    return command, args[1:]


commands: Dict[str, Callable[[List[str], AppContext], str]] = {
    "hello": lambda args, ctx: "How can I help you?",
    "help": help_command,

    # Contact's commands
    "add": add_contact,
    "phone": get_contact_phones,
    "set-email": set_email,
    "set-birthday": set_birthday,
    "show-birthday": show_birthday,
    "set-address": set_address,
    "change": edit_phone,
    "delete-phone": delete_phone,
    "delete-email": delete_email,
    "delete-birthday": delete_birthday,
    "delete-address": delete_address,
    "find": find_contacts,
    "all": all_contacts,
    "birthdays": upcoming_birthdays,
    "delete-contact": delete_contact,

    # Note's commands
    "add-note": add_note,
    "note": get_note,
    "notes": all_notes,
    "edit-note-title": edit_note_title,
    "edit-note-body": edit_note_body,
    "edit-note-tags": edit_note_tags,
    "find-notes": find_notes,
    "find-notes-tags": find_notes_by_tags,
    "sort-notes-tags": sort_notes_by_tags,
    "delete-note": delete_note,
}


@input_error
def handle_command(user_input: str, ctx: AppContext) -> str:
    """Process a user command and return the result or error message."""
    command, args = parse_input(user_input)

    match command:
        case "close" | "exit":
            return "exit"
        case cmd if cmd in commands:
            return commands[cmd](args, ctx)
        case _:
            available = f'{Out.RESET}, {Out.COMMAND}'.join(sorted(commands.keys()) + ['close', 'exit'])
            return f"{Out.ERROR}Invalid command.{Out.RESET}\nAvailable commands: {Out.COMMAND}{available}{Out.RESET}"


def get_available_commands():
    """Return a list of all available command strings."""
    return commands.keys()

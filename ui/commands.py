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
    if len(args) < 2:
        raise ValueError("add command requires 2 arguments: username and phone")

    name = args[0]
    phone = " ".join(args[1:])

    res = ctx.contacts.add_contact_or_phone(name, phone)
    return {
        "contact": f"Contact {name} was added to the book.",
        "phone": f"Phone was added to the contact {name}."
    }.get(res, '')


def set_email(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError(
            "set-email command requires 2 arguments: username and email"
        )

    name, email, *_ = args
    ctx.contacts.set_email(name, email)
    return "Email was set for the contact."


def set_birthday(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError(
            "set-birthday command requires 2 arguments: username and birthday"
        )

    name, birthday, *_ = args
    ctx.contacts.set_birthday(name, birthday)
    return "Birthday has been set for the contact."


def show_birthday(args, ctx: AppContext):
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
    if len(args) < 2:
        raise ValueError(
            "set-address command requires 2 arguments: username and address"
        )

    username = args[0]
    address = " ".join(args[1:])
    ctx.contacts.set_address(username, address)
    return "Address was set for the contact."


def edit_phone(args, ctx: AppContext):
    if len(args) < 3:
        raise ValueError(
            "edit command requires 3 arguments: username prev phone number and new phone"
        )

    username, prev_phone, new_phone, *_ = args
    ctx.contacts.edit_phone(username, prev_phone, new_phone)
    return "Contact’s phone was successfully changed."


def delete_email(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError(
            "delete email command requires 1 arguments: username"
        )

    username = args[0]
    ctx.contacts.set_email(username, None)
    return f"Email was removed from {username}."


def delete_birthday(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError(
            "delete birthday command requires 1 arguments: username"
        )

    username = args[0]
    ctx.contacts.set_birthday(username, None)
    return f"Birthday was removed from {username}."


def delete_address(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError(
            "delete address command requires 1 arguments: username"
        )

    username = args[0]
    ctx.contacts.set_address(username, None)
    return f"Address was removed from {username}."


def find_contacts(args, ctx: AppContext):
    if not args:
        raise ValueError("Find command requires a search_text argument")

    search = " ".join(args)
    contacts = ctx.contacts.find(search)

    if not contacts:
        return f"No contact name, phone, email or birthday found for this search text: {search}"

    lines = ["Found contacts:"]
    for contact in contacts:
        lines.append(str(contact))

    return "\n".join(lines)


def all_contacts(args, ctx: AppContext):
    contacts = ctx.contacts.all()

    if not contacts:
        return Out.warn("No contacts found in the book.")

    lines = ["All contacts:"]
    for contact in contacts:
        lines.append(str(contact))
    return "\n".join(lines)


def get_contact_phones(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError(
            "get contact command requires 1 arguments: username"
        )

    username = args[0]
    contact = ctx.contacts.get(username)
    return 'Phone: ' + ', '.join([p.value for p in contact.phones])


def upcoming_birthdays(args, ctx: AppContext):
    if not args:
        raise ValueError("Command requires number of days as argument")

    try:
        num_days = int(args[0])
    except ValueError:
        raise ValueError("Number of days must be an integer")

    contacts = ctx.contacts.upcoming_birthdays(num_days)

    if not contacts:
        return Out.warn(f"No upcoming birthdays in the book for closest [{num_days}] days")

    lines = [f"Upcoming birthdays for closest [{num_days}] days:"]
    for contact, next_birthday in contacts:
        lines.append(f"{contact.name.value}: {next_birthday.strftime('%d.%m.%Y')}")
    return "\n".join(lines)


def delete_phone(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("delete-phone command requires 2 arguments: username and phone")

    name = args[0]
    phone = " ".join(args[1:])
    ctx.contacts.del_phone(name, phone)
    return f"Phone was removed from {name}."


def delete_contact(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("delete-contact command requires 1 argument: username")

    ctx.contacts.del_contact(args[0])
    return f"Contact {args[0]} deleted successfully"


# ---------- NOTE COMMANDS ----------
def _get_note_id(note_id: str):
    try:
        return int(note_id)
    except ValueError:
        raise ValueError('Note ID must be an integer')


def add_note(args, ctx: AppContext):
    if len(args) < 3:
        raise ValueError("add note command requires 3 argument: title body tags")

    title, body, tags, *_ = args
    req = CreateNoteReq(
        title=title,
        body=body.replace(r"\n", "\n"),  # allow new line symbol
        tags=tags.split(","),
    )
    note = ctx.notes.add_note(req)

    return note


def get_note(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("get note command requires 1 argument: note_id")

    note_id = _get_note_id(args[0])
    req = GetNoteReq(note_id=note_id)
    note = ctx.notes.get_note(req)

    return note


def edit_note_title(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("edit note title command requires 2 argument: note_id title")

    note_id = _get_note_id(args[0])
    title = ' '.join(args[1:])
    req = EditTitleReq(note_id=note_id, title=title)
    note = ctx.notes.edit_title(req)

    return note


def edit_note_body(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("edit note body command requires 2 argument: note_id body")

    note_id = _get_note_id(args[0])
    body = ' '.join(args[1:])

    req = EditBodyReq(note_id=note_id, body=body.replace(r"\n", "\n"))
    note = ctx.notes.edit_body(req)

    return note


def edit_note_tags(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("edit note tags command requires 2 argument: note_id tags")

    note_id = _get_note_id(args[0])
    tags = ','.join(args[1:])

    req = EditTagsReq(note_id=int(note_id), tags=tags.split(","), )
    note = ctx.notes.edit_tags(req)

    return note


def find_notes(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("find notes command requires 1 argument: query")

    query = ' '.join(args)

    req = FindReq(query=query)
    notes = ctx.notes.find(req)

    return '\n'.join([n.preview() for n in notes])


def find_notes_by_tags(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("find notes by tags command requires 1 argument: tags")

    tags = ','.join(args)
    req = FindByTagsReq(tags=tags.split(","))
    notes = ctx.notes.find_by_tags(req)

    return '\n'.join([n.preview() for n in notes])


def sort_notes_by_tags(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("sort notes by tag command requires 1 argument: tags")

    tags = ','.join(args)
    req = SortByTagsReq(tags=tags.split(","))
    notes = ctx.notes.sort_by_tags(req)

    return '\n'.join([n.preview() for n in notes])


def delete_note(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("delete note command requires 1 argument: tags")

    note_id = _get_note_id(args[0])
    ctx.notes.delete_note(DeleteReq(note_id=note_id))

    return f"Note {note_id} has been successfully deleted"


def all_notes(args, ctx: AppContext):
    notes = ctx.notes.all()

    return '\n'.join([n.preview() for n in notes])


# ---------- SYSTEM COMMANDS ----------


# flake8: noqa: E501
def help_command(args, ctx: AppContext):
    lines = []
    lines.append(Out.section("Available commands:"))
    lines.append("")
    lines.append(Out.section("# General commands"))
    lines.append(f"  {Out.cmd('hello')} - Show greeting")
    lines.append(f"  {Out.cmd('help')} - Show possible commands")
    lines.append(f"  {Out.cmd('close / exit')} - Exit the bot")
    lines.append("")
    lines.append(Out.section("# Contact's commands"))
    lines.append(f"  {Out.cmd('add', '<username> <phone>')} - Add new contact with phone or add phone to existing contact")
    lines.append(f"  {Out.cmd('change', '<username> <old_phone> <new_phone>')} - Update contact's phone")
    lines.append(f"  {Out.cmd('phone', '<username>')} - Show contact's phone number(s)")
    lines.append(f"  {Out.cmd('all')} - Show all contacts")
    lines.append(f"  {Out.cmd('find', '<search_text>')} - Find matching contacts; use * symbol to skip exact matching")
    lines.append(f"  {Out.cmd('set-birthday', '<username> <DD.MM.YYYY>')} - Set birthday to contact")
    lines.append(f"  {Out.cmd('show-birthday', '<username>')} - Show contact's birthday")
    lines.append(f"  {Out.cmd('birthdays', '<number_of_days>')} - Show upcoming birthdays in next [num] days")
    lines.append(f"  {Out.cmd('set-email', '<username> <email>')} - Set email to contact")
    lines.append(f"  {Out.cmd('set-address', '<username> <address>')} - Set address to contact")
    lines.append(f"  {Out.cmd('delete-phone', '<username> <phone>')} - Delete phone from contact")
    lines.append(f"  {Out.cmd('delete-email', '<username>')} - Delete contact's email address")
    lines.append(f"  {Out.cmd('delete-birthday', '<username>')} - Delete contact's birthday address")
    lines.append(f"  {Out.cmd('delete-address', '<username>')} - Delete contact's address address")
    lines.append(f"  {Out.cmd('delete-contact', '<username>')} - Delete contact")
    lines.append("")
    lines.append(Out.section("# Note's commands"))
    lines.append(f"  {Out.cmd('add-note', '<note>')} - Add note, returns created note")
    lines.append(f"  {Out.cmd('note', '<note-id>')} - Show title, body, tags of the note")
    lines.append(f"  {Out.cmd('notes')} - Show all notes")
    lines.append(f"  {Out.cmd('edit-note-title', '<note-id> <new-title>')} - Change note's title")
    lines.append(f"  {Out.cmd('edit-note-body', '<note-id> <new-body>')} - Change note's body")
    lines.append(f"  {Out.cmd('edit-note-tags', '<note-id> <tags>')} - Change note's tags(comma separated list)")
    lines.append(f"  {Out.cmd('find-notes', '<query>')} - Find notes that contain (title/body) specified string")
    lines.append(f"  {Out.cmd('find-notes-tags', '<tags>')} - Find notes that have one of specifed tags")
    lines.append(f"  {Out.cmd('sort-notes-tags', '<tags>')} - Sort notes by tags")
    lines.append(f"  {Out.cmd('delete-note', '<note-id>')} - Delete note by note-id")
    print("\n".join(lines))


def exit_command(ctx: AppContext):
    # TODO: save records before close
    # ctx.contacts.save()
    # ctx.notes.save()
    return "exit"


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    args = shlex.split(user_input)
    if not args:
        return "", []
    command = args[0].lower()
    return command, args[1:]


commands: Dict[str, Callable[[List[str], AppContext], str]] = {
    "hello": lambda args, ctx: Out.success("How can I help you?"),
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
    command, args = parse_input(user_input)

    match command:
        case "close" | "exit":
            return exit_command(ctx)
        case cmd if cmd in commands:
            return commands[cmd](args, ctx)
        case _:
            available = ', '.join(sorted(commands.keys()) + ['close', 'exit'])
            return f"Invalid command. Available commands: {available}"

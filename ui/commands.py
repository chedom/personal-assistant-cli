import shlex
from typing import Dict, List, Tuple, Callable
from core.app_context import AppContext

from ui.error_util import input_error

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

    ctx.contacts.add_contact(args[0], args[1])


def set_email(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("set-email command requires 2 arguments: username and email")

    ctx.contacts.set_email(args[0], args[1])


def set_birthday(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("set-birthday command requires 2 arguments: username and birthday")

    ctx.contacts.set_birthday(args[0], args[1])


def set_address(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("set-address command requires 2 arguments: username and address")

    ctx.contacts.set_address(args[0], args[1])


# ---------- NOTE COMMANDS ----------

def add_note(args, ctx: AppContext):
    if len(args) < 3:
        raise ValueError("add note command requires 3 argument: title body tags")

    title, body, tags = args
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

    req = GetNoteReq(note_id=int(args[0]))
    note = ctx.notes.get_note(req)

    return note


def edit_note_title(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("edit note title command requires 2 argument: note_id title")

    note_id, title = args

    req = EditTitleReq(note_id=int(note_id), title=title)
    note = ctx.notes.edit_title(req)

    return note


def edit_note_body(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("edit note body command requires 2 argument: note_id body")

    note_id, body = args

    req = EditBodyReq(note_id=int(note_id), body=body.replace(r"\n", "\n"))
    note = ctx.notes.edit_body(req)

    return note


def edit_note_tags(args, ctx: AppContext):
    if len(args) < 2:
        raise ValueError("edit note tags command requires 2 argument: note_id tags")

    note_id, tags = args

    req = EditTagsReq(note_id=int(note_id), tags=tags.split(","),)
    note = ctx.notes.edit_tags(req)

    return note


def find_notes(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("find notes command requires 1 argument: query")

    req = FindReq(query=args[0])
    notes = ctx.notes.find(req)

    return '\n'.join([n.preview() for n in notes])


def find_notes_by_tags(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("find notes by tags command requires 1 argument: tags")

    req = FindByTagsReq(tags=args[0].split(","))
    notes = ctx.notes.find_by_tags(req)

    return '\n'.join([n.preview() for n in notes])


def sort_notes_by_tags(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("sort notes by tag command requires 1 argument: tags")

    req = SortByTagsReq(tags=args[0].split(","))
    notes = ctx.notes.sort_by_tags(req)

    return '\n'.join([n.preview() for n in notes])


def delete_note(args, ctx: AppContext):
    if len(args) < 1:
        raise ValueError("delete note command requires 1 argument: tags")

    note_id = int(args[0])
    ctx.notes.delete_note(DeleteReq(note_id=note_id))

    return f"Note {note_id} has been successfully deleted"


def all_notes(args, ctx: AppContext):
    notes = ctx.notes.all()

    return '\n'.join([n.preview() for n in notes])


# ---------- SYSTEM COMMANDS ----------
def help_command(args, ctx: AppContext):
    print("Welcome to the personal assistant tool!\n"
          "Available commands:\n"
          "  hello                                     - Show greeting\n"
          "  help                                      - Show possible commands\n"
          "  add <username> <phone>                    - Add new contact with phone or add phone to existing contact\n"
          "  change <username> <old_phone> <new_phone> - Update contact's phone\n"
          "  phone <username>                          - Show contact's phone number(s)\n"
          "  all                                       - Show all contacts\n"
          "  set-birthday <username> <DD.MM.YYYY>      - Set birthday to contact\n"
          "  show-birthday <username>                  - Show contact's birthday\n"
          "  birthdays                                 - Show upcoming birthdays within next week\n"
          "  set-email <username> <email>              - Set email to contact\n"
          "  set-address <username> <address>          - Set address to contact\n"
          "  add-note <note>                           - Add note\n"
          "  close, exit                               - Exit the bot\n")


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
    "hello": lambda args, ctx: "How can I help you?",
    # contact related cms
    "add": add_contact,
    "set-email": set_email,
    "set-birthday": set_birthday,
    "set-address": set_address,
    # notes related cmd
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
    
    "help": help_command,
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

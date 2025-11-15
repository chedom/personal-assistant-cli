from colorama import Fore, Style, init

init(autoreset=True)


class Out:
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

    # -------- ERROR -------- #
    @staticmethod
    def error(msg: str) -> str:
        return f"{Out.ERROR}Error: {msg}"

    # -------- SUCCESS -------- #
    @staticmethod
    def success(msg: str) -> str:
        return f"{Out.SUCCESS}{msg}"

    # -------- WARNING -------- #
    @staticmethod
    def warn(msg: str) -> str:
        return f"{Out.WARNING}Warning: {msg}"

    # -------- VALIDATION MESSAGES -------- #
    @staticmethod
    def validation(msg: str) -> str:
        return f"{Out.VALID}Validation: {msg}"

    # -------- LOG / SYSTEM OUTPUT -------- #
    @staticmethod
    def log(msg: str) -> str:
        return f"{Out.LOG}[LOG] {msg}"

    # -------- COMMAND HELP -------- #
    @staticmethod
    def cmd(name: str, params: str = "") -> str:
        if params:
            return f"{Out.COMMAND}{name} {Out.PARAM}{params}"
        return f"{Out.COMMAND}{name}"

    @staticmethod
    def section(title: str) -> str:
        return f"{Out.SECTION}{title}"

    # -------- CLI INPUT PROMPT -------- #
    @staticmethod
    def input_prompt(text: str) -> str:
        return f"{Out.INPUT}{text}"

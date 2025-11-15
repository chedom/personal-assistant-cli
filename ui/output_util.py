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
    RESET = Style.RESET_ALL

    # -------- ERROR -------- #
    @staticmethod
    def error(msg: str) -> str:
        return f"{Out.ERROR}Error: {msg}{Out.RESET}"

    # -------- SUCCESS -------- #
    @staticmethod
    def success(msg: str) -> str:
        return f"{Out.SUCCESS}{msg}{Out.RESET}"

    # -------- WARNING -------- #
    @staticmethod
    def warn(msg: str) -> str:
        return f"{Out.WARNING}Warning: {msg}{Out.RESET}"

    # -------- VALIDATION MESSAGES -------- #
    @staticmethod
    def validation(msg: str) -> str:
        return f"{Out.VALID}Validation: {msg}{Out.RESET}"

    # -------- LOG / SYSTEM OUTPUT -------- #
    @staticmethod
    def log(msg: str) -> str:
        return f"{Out.LOG}[LOG] {msg}{Out.RESET}"

    # -------- COMMAND HELP -------- #
    @staticmethod
    def cmd(name: str, params: str = "") -> str:
        if params:
            return f"{Out.COMMAND}{name} {Out.PARAM}{params}{Out.RESET}"
        return f"{Out.COMMAND}{name}{Out.RESET}"

    @staticmethod
    def section(title: str) -> str:
        return f"{Out.SECTION}{title}{Out.RESET}"

    # -------- CLI INPUT PROMPT -------- #
    @staticmethod
    def input_prompt(text: str) -> str:
        return f"{Out.INPUT}{text}{Out.RESET}"

    @staticmethod
    def res_attribute(text: str) -> str:
        return f"{Out.INFO}{text}{Out.RESET}"

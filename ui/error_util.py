from exceptions import AlreadyExistError, NotFoundError
from ui.output_util import Out


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (AlreadyExistError, NotFoundError) as e:
            return f"{Out.ERROR}{e.message}{Out.RESET}"

        except KeyError as e:
            return Out.error(str(e))

        except ValueError as e:
            return Out.error(str(e))

        except IndexError as e:
            return Out.error(str(e))

        # except Exception as e:
        #     return Out.error(f"{type(e).__name__}: {e}")

    return inner

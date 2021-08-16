from ..orm import Session


def inject_session(fn):

    def injector(*args, **kwargs):
        with Session() as session:
            return fn(*args, session, **kwargs)

    return injector

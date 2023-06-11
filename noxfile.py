import nox
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session) -> None:
    session.run(*"pip install .[dev]".split())


@nox.session
def test(session: nox.Session) -> None:
    login_testuser1(session)
    run_pytest(session)


@nox.session
def docs(session: nox.Session) -> None:
    build_docs(session)

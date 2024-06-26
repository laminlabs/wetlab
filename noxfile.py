import nox
from laminci.nox import build_docs, run, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session) -> None:
    run(session, "uv pip install --system .[dev]")


@nox.session
def test(session: nox.Session) -> None:
    run_pytest(session)


@nox.session
def docs(session: nox.Session) -> None:
    build_docs(session)

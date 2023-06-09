from pathlib import Path

import nox
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def build(session):
    login_testuser1(session)
    session.install(".[dev,test]")
    run_pytest(session)
    build_docs(session)

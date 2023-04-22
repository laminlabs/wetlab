from pathlib import Path

import nox
from laminci import move_built_docs_to_docs_slash_project_slug
from laminci.nox import (
    build_docs,
    login_testuser1,
    run_pre_commit,
    run_pytest,
    setup_test_instances_from_main_branch,
)

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
def build(session):
    login_testuser1(session)
    setup_test_instances_from_main_branch(session, schema="bionty,lamin1")
    session.install(".[dev,test]")
    Path("./lnschema_lamin1/migrations/versions").mkdir(parents=True, exist_ok=True)
    run_pytest(session)
    build_docs(session)
    move_built_docs_to_docs_slash_project_slug()

import nox
from laminci.nox import (
    SYSTEM,
    build_docs,
    install_lamindb,
    run,
    run_pre_commit,
    run_pytest,
)

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def install(session: nox.Session) -> None:
    run(session, f"uv pip install {SYSTEM} --upgrade scanpy")
    install_lamindb(session, branch="main", extras="bionty,aws,jupyter,ourprojects")
    run(
        session,
        f"uv pip install {SYSTEM} --no-deps git+https://github.com/laminlabs/cellxgene-lamin",
    )
    run(session, f"uv pip install {SYSTEM} .[dev]")


@nox.session
def test(session: nox.Session) -> None:
    run_pytest(session, coverage=False)


@nox.session
def docs(session: nox.Session) -> None:
    run(session, "lamin init --storage ./docsbuild --schema bionty,wetlab")
    build_docs(session, strict=True)

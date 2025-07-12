import nox


@nox.session(python="3.13")
def tests(session):
    """Run the test suite."""
    session.install("-e", ".[dev]")
    session.run("pytest", "tests/", "-v")


@nox.session
def lint(session):
    """Run linting tools."""
    session.install("ruff")
    session.run("ruff", "check", "app/", "tests/")


@nox.session
def format_code(session):
    """Format code with ruff."""
    session.install("ruff")
    session.run("ruff", "format", "app/", "tests/")
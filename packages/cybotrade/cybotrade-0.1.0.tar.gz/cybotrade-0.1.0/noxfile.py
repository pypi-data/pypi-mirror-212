import nox


@nox.session
def python(session):
    session.install("-rrequirements-dev.txt")
    session.install("cybotrade")
    session.run_always("cybotrade", "develop")
    session.run("pytest")

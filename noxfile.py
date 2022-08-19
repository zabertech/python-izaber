import nox
import pathlib

PACKAGE_BUILT = False

DB_CREATED = False

CURRENT_PATH = pathlib.Path(__file__).parent

@nox.session()
def build(session):
    global PACKAGE_BUILT
    PACKAGE_BUILT = True
    session.run("poetry", "build", )

@nox.session(python=['pypy3', '3.6', '3.7', '3.8', '3.9', '3.10', '3.11' ])
def tests(session):
    global PACKAGE_BUILT

    session.chdir(CURRENT_PATH/"tests")

    #session.run("python", "/root/install-poetry.py")
    #session.install("pytest")

    # Build the package if not built yet in this session
    #if not PACKAGE_BUILT:
    #    session.run("poetry", "build", external=True)
    #    PACKAGE_BUILT = True
    session.run("poetry", "install", external=True)

    # Install the package
    #dist_path = pathlib.Path('dist')
    #wheels = sorted(dist_path.glob('*.whl'))
    #newest_wheel = str(wheels[-1].resolve())
    #session.install(newest_wheel)

    # Install the modules that are required for our tests
    #session.install('pytest>=4.6.11','Faker>=13.3.4','passlib>=1.7.4')

    # Finally, run the tests
    session.run("pytest")


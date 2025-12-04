from loader import *
from server import *
from security import *

if __name__ == "__main__" and satisfiedLibs():

    # loadContents()
    app.secret_key = secret_key()
    app.run()



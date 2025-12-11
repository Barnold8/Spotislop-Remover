from loader import *
from server import *
from security import *
import data
if __name__ == "__main__" and satisfiedLibs():

    app.secret_key = secret_key()
    app.run()
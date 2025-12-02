installString = "Try running \"pip install -r requirements.txt\" from the \"contents directory\"."

def printLibError(lib, installString):
    print(f"Missing library \"{lib}\". {installString}")
    exit(1)

try:
    import flask
except ImportError:
    printLibError("flask",installString)

try:
    import requests
except ImportError:
    printLibError("requests",installString)
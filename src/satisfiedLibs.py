import pkg_resources

def satisfiedLibs() -> bool:

    required  = None
    satisfied = True
    installString = "Try running \"pip install -r requirements.txt\" from the \"contents\" directory."

    with open("../contents/requirements.txt") as requirements:
        required = requirements.readlines()
        
    for package in required:
        try:
            dist = pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            print(f"Could not find the lib {package}")
            satisfied = False
            
    if satisfied == False:
        print("\n"+installString)

    return satisfied

if not satisfiedLibs():
    exit(1)

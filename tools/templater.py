TEMPLATES_PATH = '../templates/'

def getHeader(): 
    return open(TEMPLATES_PATH + 'header.html', 'r').read()

def getNavbar():
    return open(TEMPLATES_PATH + 'navbar.html', 'r').read()
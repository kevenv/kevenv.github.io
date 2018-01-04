import subprocess as cmd

TEMPLATES_PATH = '../templates'

def main():
    pages = [
        'index',
        'about',
        'projects',
        'links',
        'contact'
    ]
    for p in pages:
        cmd.call('python -m cogapp -o ../{0}.html -d {1}/{0}.cog'.format(p,TEMPLATES_PATH), shell=True)

main()
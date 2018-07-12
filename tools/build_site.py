import pystache
import sass

TEMPLATES_PATH = 'templates'
CSS_PATH = '.'

def main():
    # MUSTACHE
    renderer = pystache.Renderer(search_dirs=TEMPLATES_PATH)

    pages = [
        'index',
        'about',
        'projects',
        'links',
        'contact',
        'project_chip8',
        'project_europa'
    ]
    for p in pages:
        outPage = renderer.render_path('{}/{}.mustache'.format(TEMPLATES_PATH,p))
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH),
            {'body':outPage, 'pageName': p})
        with open('{}.html'.format(p),'w') as f:
            f.write(out)

    # SASS
    sass.compile(dirname=(TEMPLATES_PATH,CSS_PATH), output_style='compressed')

main()
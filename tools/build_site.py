import pystache

TEMPLATES_PATH = 'templates'

def main():
    renderer = pystache.Renderer(search_dirs=TEMPLATES_PATH)

    pages = [
        'index',
        'about',
        'projects',
        'links',
        'contact'
    ]
    for p in pages:
        outPage = renderer.render_path('{}/{}.mustache'.format(TEMPLATES_PATH,p))
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH),
            {'body':outPage, 'pageName': p})
        f = open('{}.html'.format(p),'w')
        f.write(out)
        f.close()

main()
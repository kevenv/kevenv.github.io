import pystache
import sass
import markdown

TEMPLATES_PATH = 'templates'
CSS_PATH = '.'

def main():
    # MUSTACHE
    renderer = pystache.Renderer(search_dirs=TEMPLATES_PATH)

    # MARKDOWN
    extension_configs = {
        'codehilite': {
            'linenums': True,
            'guess_lang': False,
            'use_pygments': True
        }
    }
    md = markdown.Markdown(
        extensions=['tables','fenced_code','codehilite','markdown_katex'],
        extension_configs=extension_configs)
    header = '''
    <link rel="stylesheet" href="codehilite.css">
    '''

    # SASS
    sass.compile(dirname=(TEMPLATES_PATH,CSS_PATH), output_style='compressed')

    pages = [
        'index',
        'about',
        'projects',
        'blog',
        'contact',
        'project_chip8',
        'project_europa',
        'master_thesis'
    ]
    for p in pages:
        print(p)
        outPage = renderer.render_path('{}/{}.mustache'.format(TEMPLATES_PATH,p))
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH),
            {'body':outPage, 'pageName': p})
        with open('{}.html'.format(p),'w') as f:
            f.write(out)
    
    posts = [
        'hello'
    ]
    for p in posts:
        print('blog/{}'.format(p))

        with open('{}/blog/{}.md'.format(TEMPLATES_PATH,p),'r') as f:
            text = f.read()
        outPage = md.reset().convert(text)
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH),
            {'body':outPage, 'pageName': 'blog', 'head': header})
        with open('blog_{}.html'.format(p),'w') as f:
            f.write(out)

main()

import pystache
import sass
import markdown

TEMPLATES_PATH = 'templates'
IMAGES_PATH = 'imgs'
DOCS_PATH = 'docs'
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
        ('index',''),
        ('about',''),
        ('projects',''),
        ('publications',''),
        # ('blog',''),
        ('contact',''),
        ('projects/chip8','../'),
        ('projects/europa','../'),
        ('publications/master_thesis','../'),
        ('publications/volume_product_sampling','../'),
    ]
    for page in pages:
        print(page)
        
        p = page[0]
        root = page[1]
        root_images = root + IMAGES_PATH + '/'
        root_docs = root + DOCS_PATH + '/'
        
        outPage = renderer.render_path('{}/{}.mustache'.format(TEMPLATES_PATH,p), {
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH), {
            'body':outPage, 'pageName': p,
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        with open('{}.html'.format(p),'w') as f:
            f.write(out)
    
    '''
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
    '''

main()

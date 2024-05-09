import textwrap
import pystache
import markdown

TEMPLATES_PATH = 'templates'
IMAGES_PATH = 'imgs'
DOCS_PATH = 'docs'

if __name__ == '__main__':
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
        extension_configs=extension_configs
    )

    # HTML
    pages = [
        ('index',''),
        ('about',''),
        ('projects',''),
            ('projects/chip8','../'),
            ('projects/europa','../'),
        ('publications',''),
            ('publications/master_thesis','../'),
            ('publications/volume_product_sampling','../'),
            ('publications/ddm_compression','../'),
        ('blog',''),
    ]
    for page in pages:
        print(page)
        
        p = page[0]
        root = page[1]
        root_images = root + IMAGES_PATH + '/'
        root_docs = root + DOCS_PATH + '/'
        
        out_page = renderer.render_path('{}/{}.mustache'.format(TEMPLATES_PATH,p), {
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        if not 'publications/' in p:
            # TODO: hacky way to avoid indenting <pre>
            out_page = textwrap.indent(out_page, 8 * ' ')
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH), {
            'body': out_page, 'pageName': p,
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        with open('{}.html'.format(p),'w') as f:
            f.write(out)
    
    # BLOG
    posts = [
        'hello'
    ]
    for p in posts:
        print('blog/{}'.format(p))

        with open('{}/blog/{}.md'.format(TEMPLATES_PATH,p),'r') as f:
            text = f.read()
        out_page = '<link rel="stylesheet" href="codehilite.css">\n'
        out_page += md.reset().convert(text)
        # TODO: hacky way to avoid indenting <pre>
        # out_page = textwrap.indent(out_page, 8 * ' ')
        # extract header from body
        idx = out_page.find("</style>") + 8
        header = out_page[0:idx]
        out_page = out_page[idx:]
        out = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH),
            { 'body': out_page, 'pageName': 'blog', 'head': header }
        )
        with open('blog_{}.html'.format(p),'w') as f:
            f.write(out)

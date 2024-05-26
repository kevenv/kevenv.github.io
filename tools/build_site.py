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
            ('blog/cuda_hello','../'),
            # ('blog/zip_format','../'),
            # ('blog/hello','../'),
            # ('blog/heat_equation','../'),
    ]
    for page in pages:
        print(page)
        
        p = page[0]
        root = page[1]
        root_images = root + IMAGES_PATH + '/'
        root_docs = root + DOCS_PATH + '/'
        
        if 'blog/' in p:
            page_md = renderer.render_path('{}/{}.md'.format(TEMPLATES_PATH,p), {
                'root': root, 'rootImages': root_images, 'rootDocs': root_docs
            })
            page_html = '<link rel="stylesheet" href="{}style/codehilite.css">\n'.format(root)
            page_html += md.reset().convert(page_md)
            # extract head from body
            idx = page_html.find("<h1>")
            head = page_html[0:idx]
            page_html = page_html[idx:]
        else:
            head = ''
            page_html = renderer.render_path('{}/{}.mustache'.format(TEMPLATES_PATH,p), {
                'root': root, 'rootImages': root_images, 'rootDocs': root_docs
            })
        # TODO: hacky way to avoid indenting <pre>
        if (not 'publications/' in p) and (not 'blog/' in p):
            page_html = textwrap.indent(page_html, 8 * ' ')
        page_html = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH), {
            'body': page_html, 'pageName': p, 'head': head,
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        with open('{}.html'.format(p),'w') as f:
            f.write(page_html)

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
        ('index','','Home'),
        ('about','','About'),
        ('projects','','Projects'),
            ('projects/chip8','../','Projects Chip8'),
            ('projects/europa','../','Project Europa'),
        ('publications','','Publications'),
            ('publications/master_thesis','../','Master\'s Thesis'),
            ('publications/volume_product_sampling','../','Volume Product Sampling'),
            ('publications/ddm_compression','../','DDM Compression'),
        ('blog','','Blog'),
            ('blog/linux_cheatsheet','../','Linux Cheatsheet'),
            ('blog/bash_cheatsheet','../','Bash Cheatsheet'),
            ('blog/git_cheatsheet','../','Git Cheatsheet'),
            ('blog/makefile_cheatsheet','../','Makefile Cheatsheet'),
            ('blog/c_style','../','C Style'),
            ('blog/cuda_hello','../','CUDA Tutorial 1 - Hello World!'),
            ('blog/sort_algos','../','Sorting algorithms'),
            ('blog/why_linux','../','Why Linux'),
            ('blog/priority_queue','../','Priority Queue'),
            ('blog/bmp_format','../','BMP Image Format'),
            # ('blog/zip_format','../','ZIP Format'),
    ]
    for page in pages:
        print(page)
        
        p = page[0]
        root = page[1]
        title = page[2]
        root_images = root + IMAGES_PATH + '/'
        root_docs = root + DOCS_PATH + '/'
        
        if ('blog/' in p) or ('projects/' in p):
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
            'body': page_html, 'title': title, 'head': head,
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        with open('{}.html'.format(p),'w') as f:
            f.write(page_html)

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
            ('courses','','Courses'),
            ('history','','History'),
        ('projects','','Projects'),
            ('projects/parkhere','../','parkhere'),
            ('projects/wavesim','../','wavesim'),
            ('projects/neon','../','neon'),
            ('projects/europa','../','europa'),
            ('projects/vehiculus','../','vehiculus'),
            ('projects/flicker','../','flicker'),
            ('projects/tinyv','../','tinyv'),
        ('publications','','Publications'),
            ('publications/master_thesis','../','Master\'s thesis'),
            ('publications/volume_product_sampling','../','Volume product sampling'),
            ('publications/ddm_compression','../','DDM compression'),
        ('blog','','Blog'),
            ('blog/cuda_setup','../','CUDA Tutorial 1 - Setup!'),

            ('blog/bmp_format','../','BMP image format'),
            ('blog/qoi_format','../','QOI image format'),
            ('blog/tar_format','../','Tar file format'),
            ('blog/chip8','../','Chip8 emulator'),
            # ('blog/zip_format','../','ZIP format'),
        ('notes','','Notes'),
            ('notes/linux_cheatsheet','../','Linux cheatsheet'),
            ('notes/bash_cheatsheet','../','Bash cheatsheet'),
            ('notes/git_cheatsheet','../','Git cheatsheet'),
            ('notes/makefile_cheatsheet','../','Makefile cheatsheet'),
            ('notes/c_style','../','C style'),
            ('notes/bit_ops','../','Bitwise operations'),
            ('notes/css_cheatsheet','../','CSS cheatsheet'),
            ('notes/fedora_setup','../','Fedora setup'),
            ('notes/fedora_nvidia','../','Fedora + Nvidia'),

            ('notes/sort_algos','../','Sorting algorithms'),
            ('notes/priority_queue','../','Priority queue'),
            ('notes/why_linux','../','Why Linux'),
            ('notes/nnet_backprop','../','Backprop'),
    ]
    for page in pages:
        print(page)
        
        p = page[0]
        root = page[1]
        title = page[2]
        root_images = root + IMAGES_PATH + '/'
        root_docs = root + DOCS_PATH + '/'

        markdown_dirs = ['blog/', 'projects/', 'notes/']
        if any(s in p for s in markdown_dirs):
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
        pre_dirs = ['blog/', 'publications/', 'notes/']
        if all(s not in p for s in pre_dirs):
            page_html = textwrap.indent(page_html, 8 * ' ')
        page_html = renderer.render_path('{}/layout.mustache'.format(TEMPLATES_PATH), {
            'body': page_html, 'title': title, 'head': head,
            'root': root, 'rootImages': root_images, 'rootDocs': root_docs
        })
        with open('{}.html'.format(p),'w') as f:
            f.write(page_html)

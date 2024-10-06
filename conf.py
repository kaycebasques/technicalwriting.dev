author = 'Kayce Basques'
copyright = '2024, Kayce Basques'
exclude_patterns = [
    '.github',
    '.gitignore',
    '_build',
    'Makefile',
    'README.md',
    'boostrap.sh',
    'mdx',
    'requirements.txt',
    'venv'
]
extensions = [
    'sphinx_reredirects'
]
html_extra_path = [
    'rss.xml'
]
html_permalinks_icon = '#'
html_static_path = ['_static']
project = 'technicalwriting.dev'
pygments_style = 'sphinx'
redirects = {
    'www/pdf': '../ux/pdf.html'
}
release = '0.0.0'
templates_path = ['_templates']

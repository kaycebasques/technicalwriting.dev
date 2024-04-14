project = 'technicalwriting.dev'
copyright = '2024, Kayce Basques'
author = 'Kayce Basques'
release = '0.0.0'

extensions = []
templates_path = ['_templates']
exclude_patterns = [
    '.github',
    '.gitignore',
    'Makefile',
    'README.md',
    '_build',
    'boostrap.sh',
    'mdx',
    'play.rst',
    'plugins.rst',
    'principles.rst',
    'requirements.txt',
    'venv'
]
pygments_style = 'sphinx'

html_static_path = ['_static']
html_extra_path = [
    'rss.xml'
]
html_permalinks_icon = '#'

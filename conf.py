author = 'Kayce Basques'
copyright = '2025, Kayce Basques'
exclude_patterns = [
    '.github',
    '.gitignore',
    '_build',
    'Makefile',
    'README.md',
    'boostrap.sh',
    'data/anchors.rst',
    'mdx',
    'requirements.txt',
    'venv'
]
extensions = [
    'matplotlib.sphinxext.plot_directive',
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
    'data/embeddings': '../embeddings/overview.html',
    'data/intertwingularity': '../links/intertwingularity.html',
    'seo/sentry-overflow': '../archives/seo/sentry-overflow.html',
    'src/link-text-automation': '../links/automation.html',
    'src/verbatim-wrangling': 'https://web.archive.org/web/20240724083629/https://technicalwriting.dev/src/verbatim-wrangling.html',
    'ux/offline': '../archives/ux/offline.html',
    'ux/pdf': '../links/pdf.html',
    'www/pdf': '../links/pdf.html'
}
release = '0.0.0'
templates_path = ['_templates']
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html#configuration-options
plot_html_show_formats = False

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
    'a11y/skip': '../archives/a11y/skip.html',
    'data/embeddings': '../embeddings/overview.html',
    'data/intertwingularity': '../links/intertwingularity.html',
    'embeddings/overview': '../ml/embeddings/overview.html',
    'ml/plugins': '../archives/ml/plugins.html',
    'seo/discovered-not-indexed': '../archives/seo/discovered-not-indexed.html',
    'seo/sentry-overflow': '../archives/seo/sentry-overflow.html',
    'src/link-text-automation': '../links/automation.html',
    'src/verbatim-wrangling': 'https://web.archive.org/web/20240724083629/https://technicalwriting.dev/src/verbatim-wrangling.html',
    'ux/offline': '../archives/ux/offline.html',
    'ux/pdf': '../links/pdf.html',
    'ux/methodology': '../archives/ux/methodology.html',
    'ux/searchboxes': '../archives/ux/searchboxes.html',
    'www/pdf': '../links/pdf.html'
}
release = '0.0.0'
templates_path = ['_templates']
# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html#configuration-options
plot_html_show_formats = False

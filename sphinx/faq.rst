How to get docname in doctree-read event handler

def doctree_read(app, doctree):
    docname = app.env.current_document.docname
    core.doctree_read(docname, doctree)

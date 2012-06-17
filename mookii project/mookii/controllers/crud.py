"""Creates html element/links for inclusion in crud datagrid.
Last Update Info: $Id: crud.py 286 2007-04-27 11:39:04Z daxoffice $
"""
from elementtree import ElementTree

def show_link(record):
    link = ElementTree.Element('a',href='show/%s' % str(record.id))
    link.text = 'Show'
    return link

def edit_link(record):
    link = ElementTree.Element('a',href='edit/%s' % str(record.id))
    link.text = 'Edit'
    return link

def destroy_link(record):
    link = ElementTree.Element('a',href='destroy/%s' % str(record.id),onclick="""if (confirm('Are you sure?')) { var f = document.createElement('form'); this.parentNode.appendChild(f); f.method = 'POST'; f.action = this.href; f.submit(); };return false;""")
    link.text = 'Destroy'
    return link


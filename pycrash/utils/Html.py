from lxml import etree
from mako.template import Template
from mako import exceptions

import os


def XMLtoHTML(xml):
    tree = etree.fromstring(xml)

    filename = os.path.join(os.path.dirname(__file__), "template.mako")

    mytemplate = Template(filename=filename)

    try:
        return mytemplate.render(crash=tree)
    except:
        return  exceptions.html_error_template().render()


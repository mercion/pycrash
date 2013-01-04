from lxml import etree
from mako.template import Template
from mako import exceptions


def XMLtoHTML(xml):
    tree = etree.fromstring(xml)
    root = tree.getroot()

    mytemplate = Template(filename="template.mako")

    try:
        return mytemplate.render(crash=tree.getroot())
    except:
        return  exceptions.html_error_template().render()


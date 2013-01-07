
#rom distutils.core import setup
from setuptools import setup

setup(  name="PyCrash",
      	version="1.0PreAlpha1",
		description="PyCrash: a Run-Time Exception Dumper for Python programs",
		author="Carmine I.D. Noviello, Mercion Wilathgamuwage",
		author_email="mwilathg@cisco.com",
		url="http://www.pycrash.org",
		packages=['pycrash', 'pycrash.utils'])

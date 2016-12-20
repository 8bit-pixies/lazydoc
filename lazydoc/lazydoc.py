"""
lazy doc module

This module guesses the information and tries to generate the 
information based on the sphinx quickstart.

Currently depends on setup.cfg to be populated to work - in future iterations
this can probably be infered from the package information somehow


Other implementations:

*  https://bitbucket.org/etienned/sphinx-autopackage-script/src/7199e97257891b60345cb4d3f8b4109442c12c01/generate_modules.py?at=default&fileviewer=file-view-default

"""


import os, sys
import subprocess
import argparse

def cleanup():
    """removes the doc folder to clean up the mess"""
    from shutil import rmtree
    try:
        rmtree("doc")
    except:
        pass

if (sys.version_info > (3, 0)):
    import configparser
    config = configparser.ConfigParser()
    config.read('C:/users/chapm/documents/github/lazydoc/setup.cfg')
else:
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read(open('C:/users/chapm/documents/github/lazydoc/setup.cfg', 'r'))

version = config.get('metadata', 'version')
project = config.get('metadata', 'name')
author = config.get('metadata', 'author')

def generate():
    """this is the initial generation using sphinx-quickstart"""
    quickstart = [
    'sphinx-quickstart', 
    'doc', 
    '-q', 
    '-p', 
    '"{project}"'.format(project=project), 
    '-a',
    '"{author}"'.format(author=author), 
    '-v',
    '"{version}"'.format(version=version), 
    '--ext-autodoc', 
    '--extensions=sphinx.ext.autosummary'
    ]

    recommonmark_settings = """
from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']
import sys
import os
sys.path.append("C:/users/chapm/documents/github/lazydoc")
"""

    cleanup()
    subprocess.call(quickstart)

    with open('doc/conf.py', 'a') as f:
        f.write(recommonmark_settings)
        
####try:
####    copyfile(os.join("doc", "index.rst"), os.join("doc", "contents.rst"))
####except:
####    pass
####    
####try:
####    copyfile(os.join("doc", "contents.rst"), os.join("doc", "index.rst"))
####except:
####    pass

def document():
    """generates documentation automatically"""
    # generate doc stuff
    gen_docs = [
    'sphinx-apidoc',     
    '-o', 
    'doc', 
    project, 
    '--force'
    ]
    make_html = [
    'make',
    'html'
    ]
    print(gen_docs)
    subprocess.call(gen_docs)
    os.chdir("doc")    
    print(make_html)
    subprocess.call(make_html)
    os.chdir("..")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('type')
    args = parser.parse_args()
    
    if args.type.startswith("doc"):
        document()
    elif args.type.startswith("gen"):
        generate()
    else:
        print("Please enter 'generate' or 'document'")
        raise

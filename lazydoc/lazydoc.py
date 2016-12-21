"""
lazy doc module

This module guesses the information and tries to generate the 
information based on the sphinx quickstart.

Other implementations:

*  https://bitbucket.org/etienned/sphinx-autopackage-script/src/7199e97257891b60345cb4d3f8b4109442c12c01/generate_modules.py?at=default&fileviewer=file-view-default

"""


import os, sys
import subprocess

def cleanup():
    """Removes the doc folder to clean up the sphinx docs"""
    from shutil import rmtree
    try:
        rmtree("doc")
    except:
        pass

def get_config(input='setup.cfg'):
    """Extract the metadata from the appropriate config file. 
    
    Supports `setup.cfg` and reading in `yaml` related files.
    """
    if input.endswith('cfg'):
        if (sys.version_info > (3, 0)):
            import configparser
            config = configparser.ConfigParser()
            config.read(input)
        else:
            import ConfigParser
            config = ConfigParser.ConfigParser()
            config.read(open(input, 'r'))

        version = config.get('metadata', 'version')
        project = config.get('metadata', 'name')
        author = config.get('metadata', 'author')
    elif input.endswith('yml') or input.endswith('yaml'):
        with open(input, 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        version, project, author = cfg['version'], cfg['project'], cfg['author']
    return version, project, author

def generate():
    """Generate the sphinx quickstart settings based on biased defaults"""
    version, project, author = get_config()
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
sys.path.insert(0, os.path.abspath('..'))
"""
    cleanup()
    subprocess.call(quickstart)

    with open('doc/conf.py', 'a') as f:
        f.write(recommonmark_settings)
        
def document():
    """(Re)generate all documentation."""
    version, project, author = get_config()
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

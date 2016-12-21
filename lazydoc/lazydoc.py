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
    """removes the doc folder to clean up the sphinx docs"""
    from shutil import rmtree
    try:
        rmtree("doc")
    except:
        pass

def get_config():
    """extracts the relevant meta data
    
    Future todo:
    extract metadata when it is missing from `setup.cfg`    
    """
    if (sys.version_info > (3, 0)):
        import configparser
        config = configparser.ConfigParser()
        config.read('setup.cfg')
    else:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        config.read(open('setup.cfg', 'r'))

    version = config.get('metadata', 'version')
    project = config.get('metadata', 'name')
    author = config.get('metadata', 'author')
    return version, project, author

def generate():
    """this is the initial generation using sphinx-quickstart"""
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
    """generates documentation automatically"""
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

def main():
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

if __name__ == "__main__":
    main()
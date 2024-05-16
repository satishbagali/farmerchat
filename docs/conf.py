# Configuration file for the Sphinx documentation builder. 
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

autodoc_mock_imports = ["peewee"]

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath('../database'))
sys.path.insert(0, os.path.abspath('../database/models'))
sys.path.insert(0, os.path.abspath('../common'))
sys.path.insert(0, os.path.abspath('../django_core/'))
sys.path.insert(0, os.path.abspath('../django_core/config'))

project = 'Agri Chat'
copyright = '2024, DigitalGreen'
author = 'DigitalGreen'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [ "sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

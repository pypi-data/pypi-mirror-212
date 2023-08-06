import pypandoc
from setuptools import setup, find_packages

setup(name="predictapi",
      version="0.0.18",
      author="The predict API",
      description=pypandoc.convert('README.md', 'rst'),
      install_requires=["requests", "numpy"],
      py_modules=['predictapi'],
      python_requires='>=3.7')


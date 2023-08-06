from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()
    
setup(name="predictapi",
      version="0.0.21",
      author="The predict API",
      description="The predict API",
      include_package_data = True,
      long_description = long_description,
      long_description_content_type="text/markdown",
      install_requires=["requests", "numpy"],
      py_modules=['predictapi'],
      python_requires='>=3.7')


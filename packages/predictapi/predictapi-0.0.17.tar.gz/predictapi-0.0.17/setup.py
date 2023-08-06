from setuptools import setup, find_packages

setup(name="predictapi",
      version="0.0.17",
      author="The predict API",
      description="The predcit API",
      install_requires=["requests", "numpy"],
      py_modules=['predictapi'],
      python_requires='>=3.7')


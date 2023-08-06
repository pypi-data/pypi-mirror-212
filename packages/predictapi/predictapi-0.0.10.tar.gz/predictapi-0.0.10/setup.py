from setuptools import setup, find_packages

setup(name="predictapi",
      version="0.0.10",
      author="The predict API",
      description="The predcit API",
      install_requires=["requests"],
      py_modules=['predictapi'],
      python_requires='>=3.7')

#packages=find_packages(where="src"),
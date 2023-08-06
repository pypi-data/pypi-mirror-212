from setuptools import setup, find_packages

setup(name="predictapi",
      version="0.0.8",
      author="The predict API",
      description="The predcit API",
      install_requires=["requests"],
      python_requires='>=3.7')

#packages=find_packages(where="src"),
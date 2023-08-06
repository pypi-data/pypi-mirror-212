from setuptools import setup
    
setup(name="predictapi",
      version="0.0.20",
      author="The predict API",
      description="The predict API",
      include_package_data = True,
      install_requires=["requests", "numpy"],
      py_modules=['predictapi'],
      python_requires='>=3.7')


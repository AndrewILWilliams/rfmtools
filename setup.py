from setuptools import setup

setup(name='rfmtools',
      version='0.1',
      description='Utility functions for running and configuring the Reference Forward Model (RFM; Dudhia, 2017)',
      url='http://github.com/AndrewWilliams3142/rfmtools',
      author='Andrew Williams',
      author_email='andrew.williams@physics.ox.ac.uk',
      license='GNU',
      packages=['rfmtools'],
      install_requires=['numpy', 'matplotlib'],
      zip_safe=False)
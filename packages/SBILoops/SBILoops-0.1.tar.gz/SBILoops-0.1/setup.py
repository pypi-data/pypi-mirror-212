from setuptools import setup, find_packages


setup(
    name='SBILoops',
    version='0.1',
    license='MIT',
    author="Patrick Gohl",
    author_email='patrick.gohl@upf.edu',
    packages=find_packages('SBI'),
    package_dir={'': 'SBI'},
    url='https://github.com/structuralbioinformatics/SBI',
    keywords='Structural Bioinformatics, Loops',
    install_requires=[
          'numpy','pandas','pynion','Requests','scipy','six'
      ],

)


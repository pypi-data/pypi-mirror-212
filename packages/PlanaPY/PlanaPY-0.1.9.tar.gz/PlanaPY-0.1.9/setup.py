from setuptools import setup, find_packages


setup(
    name='PlanaPY',
    version='0.1.9',
    license='MIT',
    author='Erik Schau',
    author_email='hopfenspiel@gmail.com',
    package_dir = {'': 'src'},
    packages=find_packages(where='src'),
    description='Anaplan RESTful API Convenience Library',
    url='https://github.com/hopfenspiel/PlanaPY',
    keywords='anaplan',
    install_requires=[
          'requests',
          'pandas',
      ],

)

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='yggdrasil',
      version='0.1',
      description='A python package to create data intelligence workflow',
      url='https://github.com/adeblonde/yggdrasil',
      author='Antoine Deblonde',
      author_email='antoine.deblonde@protonmail.ch',
      license='LGPLv3',
      packages=['yggdrasil'],
      install_requires=[
          'Click',
          'python-terraform'
      ],
      entry_points={
        'console_scripts': ['ygg=yggdrasil.cli:main']
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False) 
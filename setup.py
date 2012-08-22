from setuptools import setup, find_packages
import os

version = '0.2'

def read(fname):
      return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='githook',
      version=version,
      description="Simple web application that runs a script in response of GitHub post hook.",
      long_description=read("README.rst"),
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: POSIX',
                   'Topic :: Utilities'
                  ],
      keywords='',
      author='Andraz Brodnik',
      author_email='brodul@brodul.org',
      url='https://github.com/brodul/githook',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
            "Flask",
      ],
      entry_points={'console_scripts': ['githook = githook:cli_run'] },
      )

from setuptools import setup, find_packages

version = '0.1'

setup(name='githook',
      version=version,
      description="Simple web application that runs a script in response of GitHub post hook.",
      long_description="""\
      This aplication starts a small web server, 
reads a INI config file and listens for GitHub post requests,
then runs a script in response of the post request.
""",
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

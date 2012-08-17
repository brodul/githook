from setuptools import setup, find_packages

version = '0.1'

setup(name='githook',
      version=version,
      description="Simple Flask aplication that runs a script in response of GitHub post hook.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Andraz Brodnik',
      author_email='brodul@brodul.org',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
            "Flask",
            "mock",
      ],
      entry_points={'console_scripts': ['githook = githook:cli_run'] },
      )

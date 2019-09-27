from setuptools import setup
from netstats import __version__

setup(name='netstats',
      version=__version__,
      description='Data analysis in a network provider',
      url='https://github.com/liragabriel/netstats',
      author='Gabriel Lira',
      author_email='liragabrieler@gmail.com',
      license='MIT',
      packages=['netstats'],
      install_requires=['flask', 'pandas', 'seaborn', 'matplotlib'],
      zip_safe=False)

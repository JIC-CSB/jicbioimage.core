from setuptools import setup

# Importing the "multiprocessing" module is required for the "nose.collector".
# See also: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing
except ImportError:
    pass

# Define the test runner.
# See also:
# http://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-python-setuptools-test-command/
from setuptools.command.test import test as TestCommand
class NoseTestCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly.
        import nose
        nose.run_exit(argv=['nosetests'])

version = "0.13.0"
readme = open('README.rst').read()

setup(name='jicbioimage.core',
      packages=['jicbioimage', 'jicbioimage.core', 'jicbioimage.core.util'],
      version=version,
      description='Python package designed to make it easy to work with bio images.',
      long_description=readme,
      author='Tjelvar Olsson',
      author_email = 'tjelvar.olsson@jic.ac.uk',
      url = 'https://github.com/JIC-CSB/jicbioimage.core',
      download_url = 'https://github.com/JIC-CSB/jicbioimage.core/tarball/{}'.format(version),
      license='MIT',
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Image Recognition",
      ],
      keywords = ['microscopy', 'image analysis'],
      cmdclass={'test': NoseTestCommand},
      install_requires=[
        'numpy',
        'scipy',
        'scikit-image',
      ]
)

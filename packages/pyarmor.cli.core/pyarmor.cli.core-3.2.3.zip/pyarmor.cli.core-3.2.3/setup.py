import sys
from setuptools import setup

__VERSION__ = '3.2.3'

package_dir = '../../src-v8/cli/core'
package_data = {
    "pyarmor.cli.core": ["pytransform3*", "pyarmor_runtime*"]
}

install_requires = []
if hasattr(sys, 'getandroidapilevel'):
    install_requires.append('pyarmor.cli.core.android==%s' % __VERSION__)
elif sys.platform.startswith(('freebsd', 'openbsd', 'isilon onefs')):
    install_requires.append('pyarmor.cli.core.freebsd==%s' % __VERSION__)

with open(package_dir + '/' + 'README.rst') as f:
    long_description = f.read()

setup(
    name="pyarmor.cli.core",

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    version=__VERSION__,
    description="Provide extension module pytransform3 for Pyarmor",
    long_description=long_description,

    url="https://github.com/dashingsoft/pyarmor",
    author="Jondy Zhao",
    author_email="pyarmor@163.com",
    license="Free To Use But Restricted",

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        # Pick your license as you wish
        "License :: Free To Use But Restricted",

        # Support platforms
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Topic :: Security",
        "Topic :: System :: Software Distribution",
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="protect obfuscate encrypt obfuscation distribute",

    packages=["pyarmor.cli.core"],
    package_dir={"pyarmor.cli.core": package_dir},
    package_data=package_data,
    install_requires=install_requires,
)

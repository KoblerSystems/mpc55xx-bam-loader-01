from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mpc55xx-bam-loader-g1',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.1',

    description='Upload binaries to Freescale MPC55xx or MPC56xx with the BAM serial protocol',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/KoblerSystems/mpc55xx-bam-loader-01',

    # Author details
    author='Jan Kobler, Kobler System GmbH',
    author_email='eng1@koblersystems.de',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
    ],

    # What does your project relate to?
    keywords='Freescale MPC55xx, Freescale MPC56xx, bootloader, Boot Assist Module (BAM)',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages('src', exclude=['contrib', 'docs', 'tests*']),

    package_dir = {'':'src'},
    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'pyserial',
        ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'mpc55xx-bam-loader=mpc55xx.mpc55xx_bam_01:main_01',
        ],
    },
)

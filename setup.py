import sys
from setuptools import setup, find_packages
from linkie import __version__

if not sys.version_info[0] == 3:
    sys.exit('Sorry, currently only Python 3 is supported.')

setup(
    name='linkie',
    version=__version__,
    description='Linkie looks through files for broken links using Python 3.',
    long_description=open('README.rst').read(),
    url='https://github.com/uccser/linkie',
    author=('University of Canterbury Computer'
            'Science Education Research Group'),
    author_email='csse-education-research@canterbury.ac.nz',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    keywords='link url checker',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests==2.18.4',
        'PyYaml==3.12',
    ],
    python_requires='~=3.4',
    entry_points={
        'console_scripts': [
            'linkie = linkie.linkie:main',
        ],
    }
    )

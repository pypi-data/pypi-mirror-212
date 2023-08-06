from setuptools import setup
import os.path
import re


# reading package's version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'prettyc.py')) as v_file:
    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


setup(
    name='prettyc',
    version=package_version,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    url='http://github.com/pylover/prettyc',
    description='Fork of Google\'s cpplint, modified to work only with C.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # For PyPI
    py_modules=['prettyc'],
    keywords=['lint', 'python', 'c'],
    license='BSD-3-Clause',
    entry_points={
        'console_scripts': [
            'prettyc = prettyc:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: C',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: BSD License'
    ]
)

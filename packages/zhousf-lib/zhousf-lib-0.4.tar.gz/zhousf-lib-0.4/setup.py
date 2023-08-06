# -*- coding: utf-8 -*-
# @Author  : zhousf
# @Date    : 2023/6/6 
# @Function:
"""

构建项目
python -m pip install --user --upgrade setuptools wheel
上传文件至Pypi
python -m pip install --user --upgrade twine
检查语法是否正确
python setup.py check
构建项目
python setup.py sdist bdist_wheel
Anaconda prompt中输入Pypi的账户与密码
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


NAME = 'zhousf-lib'
DESCRIPTION = 'a python library of zhousf'
URL = 'https://github.com/MrZhousf/ZhousfLib'
EMAIL = '442553199@qq.com'
AUTHOR = 'zhousf'
REQUIRES_PYTHON = '>=3.6.13'
VERSION = '0.4'


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()



setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.md', 'r', encoding='utf-8').read(),  # 默认是readme文件。
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    # REQUIRED 是项目依赖的库
    install_requires=[],
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)

# from __future__ import print_function
# from setuptools import setup, find_packages
# import version
#
# with open("README.md", "r", encoding='utf-8') as fh:
#     long_description = fh.read()
#
# setup(
#     name="zhousf-lib",
#     version=version.__version__,
#     author="zhousf",
#     author_email="442553199@qq.com",
#     description="a python library of zhousf",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     license="MIT",
#     url="https://github.com/MrZhousf/ZhousfLib",
#     packages=find_packages(),
#     include_package_data=True,
#     py_modules=['zhousflib'],
#     install_requires=[
#         "numpy <= 1.24.3",
#         ],
#     classifiers=[
#         "Topic :: Software Development :: Libraries :: Python Modules",
#         "Programming Language :: Python",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.5",
#         "Programming Language :: Python :: 3.5",
#         "Programming Language :: Python :: 3.6",
#         "Programming Language :: Python :: 3.7",
#         'Programming Language :: Python :: Implementation :: CPython',
#     ],
# )
#



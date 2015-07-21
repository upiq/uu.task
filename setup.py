from setuptools import find_packages
from setuptools import setup

VERSION = '0.0.1'

setup(
    name='uu.task',
    version=VERSION,
    author='Alex Clark',
    author_email='aclark@aclark.net',
    url='https://github.com/upiq/uu.task',
    description='Task Management and Notification System For Plone.',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()),
    license=u'''Original works in this package are licensed under the GNU
        General Public License v. 2.0. All original images, documentation,
        style-sheets, and JavaScript assets are additionally licensed under an
        MIT-style license.''',
    keywords='Plone Task Management',
    classifiers=[
        'Framework :: Plone',
        'Programming Language :: Python :: 2.7',
    ],

    include_package_data=True,
    packages=find_packages(),
    namespace_packages=['uu'],
    zip_safe=False,

    install_requires=[
        'setuptools',
        'plone.api',
        'plone.app.widgets<2.0.0',
        'plone.event',
    ],
    extras_require=dict(
        test=['plone.app.testing'],
    ),
    entry_points={
        'z3c.autoinclude.plugin': 'target = plone',
    },
)

from setuptools import find_packages
from setuptools import setup

VERSION='0.0.1'

setup(
    author='Alex Clark',
    author_email='aclark@aclark.net',
    classifiers=[
        'Framework :: Plone',
        'Programming Language :: Python :: 2.7',
    ],
    description='Task Management and Notification System For Plone.',
    entry_points={
        'z3c.autoinclude.plugin': 'target = plone',
    },
    keywords='Plone Task Management',
    license='Original works in this package are licensed under the GNU General Public License v. 2.0. All original images, documentation, style-sheets, and JavaScript assets are additionally licensed under an MIT-style license.',
    include_package_data=True,
    install_requires=[
        'setuptools',
    ],
    long_description=open('README.rst').read() + '\n' + open('CHANGES.rst').read(),
    name='uu.task',
    namespace_packages=[
        'uu',
    ],
    packages=find_packages(),
    test_suite='uu.task.tests.UUTaskTestSuite',
    url='https://github.com/upiq/uu.task',
    version=VERSION,
    zip_safe=False,
)

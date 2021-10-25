#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyautogui',
                'pillow'
]

test_requirements = ['pytest>=3', ]

setup(
    author="Cosmin Munteanu",
    author_email='munteanumihailcosmin@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
        'Environment :: X11 Applications',
        'Environment :: Web Environment',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Communications :: Email',
        'Topic :: Office/Business',
    ],
    description="Utility for making easy screenshots",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='monkeyshot',
    name='monkeyshot',
    packages=find_packages(include=['monkeyshot', 'monkeyshot.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/MihailCosmin/monkeyshot',
    version='0.1.0',
    zip_safe=False,
)

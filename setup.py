from setuptools import setup

setup(
    name='espnff',

    packages=['espnff'],

    include_package_data=True,

    version='1.4.0',

    description='Dashboard Application for Visualizing League Data using Dash by Plotly',

    author='Rich Barton, Connor Klopfer',

    author_email='rbart65@gmail.com, cklopfer10@aol.com',

    install_requires=['requests>=2.0.0,<3.0.0', 'dash', 'dash-core-components', 'dash-html-components',
                      'browser-cookie3'],

    test_suite='nose.collector',

    tests_require=['nose', 'requests_mock'],

    url='https://github.com/rbarton65/bin',

    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

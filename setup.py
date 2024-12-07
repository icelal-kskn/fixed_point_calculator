from setuptools import setup, find_packages

setup(
    name='fixed_point_iteration',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'flask',
        'flask-cors',
        'matplotlib',
        'requests',
        'jsonschema',
    ],
    author='Ikram Celal Keskin',
    author_email='200316059@ogr.cbu.edu.tr',
    description='A Fixed-Point Iteration root finding application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/icelal-kskn/fixed_point_iteration',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',

    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'fixed-point-gui=fixed_point_iteration.gui:main',
            'fixed-point-api=fixed_point_iteration.api:main',
        ],
    }
)
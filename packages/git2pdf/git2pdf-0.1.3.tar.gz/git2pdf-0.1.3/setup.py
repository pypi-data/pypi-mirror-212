from setuptools import setup

setup(
    name='git2pdf',
    version='0.1.3',
    py_modules=['main'],
    package_data={'': ['*.ttf']},  # Include any .ttf files in the module
    install_requires=[
        'requests',
        'fpdf',
    ],
    entry_points={
        'console_scripts': [
            'git2pdf=main:main',
        ],
    },
)

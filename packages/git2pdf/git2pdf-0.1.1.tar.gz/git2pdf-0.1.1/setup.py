from setuptools import setup, find_packages

setup(
    name='git2pdf',
    version='0.1.1',
    packages=find_packages(),
    package_data={'': ['*.ttf']},  # Include any .ttf files in the package
    install_requires=[
        'requests',
        'fpdf',
    ],
    entry_points={
        'console_scripts': [
            'git2pdf=git2pdf:main',
        ],
    },
)

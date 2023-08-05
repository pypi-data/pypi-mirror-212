from setuptools import setup

setup(
    name='git2pdf',
    version='0.1.5',
    packages=['git2pdf'],
    package_data={'git2pdf': ['*.ttf']},
    install_requires=[
        'requests',
        'fpdf2',
    ],
    entry_points={
        'console_scripts': [
            'git2pdf=git2pdf.main:main',
        ],
    },
)


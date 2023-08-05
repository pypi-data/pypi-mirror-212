from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ezqc',
    version='0.3',
    author='Tinger Shi & Sky Li',
    description='EZQC is a streamlined, terminal-based alternative to FastQC.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        # Add your project dependencies here
        'numpy',
        'matplotlib',
        'pandas',
        'scipy',
        'Bio',
    ],
    entry_points={
        'console_scripts': [
            'ezqc=ezqc.ezqc:main',
        ],
    },
)

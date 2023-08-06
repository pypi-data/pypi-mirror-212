from setuptools import setup
from pathlib import Path

this_directory = Path("README.md").parent
long_desc = (this_directory / "README.md").read_text()

setup(
    name='cncd_package',
    version='0.1.1',    
    description='A Python package for CNCD',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/shahzaib-raza/cncd',
    author='Shahzaib Raza',
    author_email='shahzaib.raza@cncd.org',
    license='BSD 2-clause',
    packages=['cncd_package'],
    install_requires=['numpy>=1.24.1', 'pandas>=1.5.3'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
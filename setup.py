from setuptools import setup, find_packages

setup(
    name='update-linux',
    version='1.0',
    author='tobias@randombytes',
    author_email='placeholder@example.com',
    description='Tool to quickly update your linux system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DasIstTobias/Update-Linux',
    packages=find_packages(),
    install_requires=[
        # placeholder
    ],
    entry_points={
        'console_scripts': [
            'update-linux=update_linux.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
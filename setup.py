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
    include_package_data=True,
    package_data={
        'update_linux': [
            'detect_distro.sh',
            'refresh_repos/apt.sh',
            'refresh_repos/dnf.sh',
            'refresh_repos/flatpak.sh',
            'refresh_repos/pacman.sh',
            'refresh_repos/zypper.sh',
            'update_packages/apt.sh',
            'update_packages/dnf.sh',
            'update_packages/flatpak.sh',
            'update_packages/pacman.sh',
            'update_packages/snap.sh',
            'update_packages/yay.sh',
            'update_packages/zypper-leap.sh',
            'update_packages/zypper-tumbleweed.sh',
        ],
    },
    install_requires=[
        # placeholder
    ],
    entry_points={
        'console_scripts': [
            'update-linux=update_linux.main:main',
        ],
    },
    license = "GPL-3.0-or-later",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

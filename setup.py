from setuptools import setup, find_packages

setup(
    name="auto_shutdown_steam_download",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List of dependencies
    ],
    entry_points={
        'console_scripts': [
            'auto-shutdown-steam-download=auto_shutdown_steam_download.main:main',
        ],
    },
    author="hkevint",
    description="A tool to automatically shut down or put your computer to sleep after Steam finishes downloading queued updates.",
    license="MIT",
    keywords="steam shutdown sleep",
    url="https://github.com/hkevint/auto_shutdown_steam_download",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)

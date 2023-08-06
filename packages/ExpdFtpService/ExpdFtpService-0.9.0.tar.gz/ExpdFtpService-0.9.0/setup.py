from setuptools import setup, find_packages


setup(
    name="ExpdFtpService",
    version="0.9.0",
    license='MIT',
    author="greg he",
    description="Python Module for download / upload file Ftp Server",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='download / upload ftp file',
    install_requires=[
        'loguru'
    ],
)
from setuptools import setup, find_packages


setup(
    name="ExpdMailService",
    version="0.5.0",
    license='MIT',
    author="greg he",
    description="Python Module for sending mail from internal mail server",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='sending mail',
    install_requires=[
        'loguru', 'pandas'
    ],
)
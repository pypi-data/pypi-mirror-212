from setuptools import setup, find_packages

setup(
    name='WM9L8_IMA',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        csv_to_arctic=WM9L8_IMA.etl_pipelines.csv_to_arctic:csv_to_arctic
    ''',
)
 
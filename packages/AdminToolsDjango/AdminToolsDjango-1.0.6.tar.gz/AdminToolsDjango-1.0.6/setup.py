from setuptools import setup
import os


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AdminToolsDjango',
    version='1.0.6',
    author='孙亮',
    packages=['AdminToolsDjango'],
    # install_requires=[
    #     # 'some_dependency>=1.0.0',
    # ],
    # package_data={'AdminToolsDjango': ['template-1.0/*', 'template-1.0/app_test', 'template-1.0/app_test/migrations',
    #                                    'template-1.0/project_name', 'template-1.0/static']},
    package_data={
        'AdminToolsDjango': ['template-1.0/**/*'],
    },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
)

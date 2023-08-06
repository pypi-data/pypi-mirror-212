from setuptools import setup, find_packages

setup(
    name='easy_excel_tool',
    version='1.0.0',
    packages=find_packages(),
    license='MIT',
    author='hanxinkong',
    author_email='xinkonghan@gmail.com',
    description='简易、好用的excel操作工具，兼具增删改查，表合并，导出等功能',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        # List your package's dependencies here
        'openpyxl==3.1.2',
        'pandas==1.3.5'
    ],
)

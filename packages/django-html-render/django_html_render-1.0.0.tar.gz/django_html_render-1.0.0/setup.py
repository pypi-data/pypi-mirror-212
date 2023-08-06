from setuptools import setup, find_packages

setup(
    name='django_html_render',
    version='1.0.0',
    description='django html render',
    long_description='django html render',
    author='ReimiBeta',
    author_email='reimi846@gmail.com',
    url='https://github.com/reimibeta/django_html_render',
    license='MIT',
    packages=find_packages(),
    # py_modules=['image_compress',],
    install_requires=[
        # other dependencies
        'Django==4.1.7'
    ],
    # other optional arguments
)

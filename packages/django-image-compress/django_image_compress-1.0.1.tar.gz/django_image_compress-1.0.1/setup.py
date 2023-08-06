from setuptools import setup, find_packages

setup(
    name='django_image_compress',
    version='1.0.1',
    description='A sample image compress',
    long_description='Test Long',
    author='ReimiBeta',
    author_email='reimi846@gmail.com',
    url='https://github.com/reimibeta/django_image_compress',
    license='MIT',
    packages=find_packages(),
    # py_modules=['image_compress',],
    install_requires=[
        # other dependencies
        'Pillow'
    ],
    # other optional arguments
)

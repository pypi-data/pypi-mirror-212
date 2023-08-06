from setuptools import setup, find_packages

setup(
    name='django_restframework_base64_image_field',
    version='1.0.0',
    description='django rest-framework convert image upload to base64',
    # long_description='Test Long',
    author='ReimiBeta',
    author_email='reimi846@gmail.com',
    url='https://github.com/reimibeta/django_restframework_base64_image_field',
    license='MIT',
    packages=find_packages(),
    # py_modules=['image_compress',],
    install_requires=[
        # other dependencies
        'Django==4.1.7',
        'djangorestframework==3.14.0',
        'six==1.16.0'
    ],
    # other optional arguments
)

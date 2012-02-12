from setuptools import setup, find_packages

f = open('README.md')
readme = f.read()
f.close()

setup(
    name='django-gencal',
    version='0.2',
    description='django-gencal is a resuable Django application for rendering calendars.',
    long_description=readme,
    author='Justin Lilly',
    author_email='justin@justinlilly.com',
    url='http://code.justinlilly.com/django-gencal/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=['gencal'],
    zip_safe=False,
)

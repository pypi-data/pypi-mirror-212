from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Python package to automate SQL queries, Excel spreadsheet creation, and email tasks.'

requirements = [
    'SQLAlchemy>=2.0.15',
    'pywin32>=306',
    'pandas>=2.0.2',
    'openpyxl>=3.1.2',
    'sqlparams>=5.1.0',
]

# Setting up
setup(
    name="BCHS_PopHealth",
    version=VERSION,
    author="BCHS Population Health",
    author_email="<pophealthdata@bronxcare.org>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=requirements,
    license="MIT license",
    keywords=['pophealth','taskmaster','BCHS','BronxCare'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
    ]
)
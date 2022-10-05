import setuptools

# pylint: disable=all
"""
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
"""
setuptools.setup(
    name="sync-git-repos",
    version="0.0.3",
    author="Anton Gorinenko",
    author_email="anton.gorinenko@gmail.com",
    description="Command for syncing git repos",
    long_description="See https://github.com/agorinenko/sync-git-repos",
    keywords='python, utils, git',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    extras_require={
        'test': [
            'pytest',
            'pylint'
        ]
    },
    python_requires='>=3.8',
)

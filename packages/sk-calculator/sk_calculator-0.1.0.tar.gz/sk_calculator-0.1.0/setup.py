from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sk_calculator',
    version='0.1.0',
    description='A simple calculator program',
    author='gkibria',
    long_description=long_description,
    long_description_content_type="text/markdown",  # Specify the content type as Markdown
    author_email='gkibria121@gmail.com',
    packages=find_packages(),
    install_requires=['regex'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'calculator=calculator.main:main',
        ],
    },
    keywords=['python', 'calculator', 'python calculator', 'gk calculator', 'advanced calculator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

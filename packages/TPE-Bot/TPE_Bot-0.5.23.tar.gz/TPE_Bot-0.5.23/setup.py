import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TPE_Bot", # Replace with your own username
    version="0.5.23",
    author="Ester Goh",
    description="A TPEdu personalised chatbot package",
    packages=setuptools.find_packages(),
    package_data={'': ['Data/*/*.js', 'Data/*/*.html', 'Data/*/*.json']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

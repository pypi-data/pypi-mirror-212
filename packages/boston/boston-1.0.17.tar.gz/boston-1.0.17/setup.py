import setuptools


setuptools.setup(
    name="boston", # Replace with your own username
    version="1.0.17",
    author="julmubm",
    author_email="dltpdn@gmail.com",
    description="loading boston housing price dataset like sklearn.datasets.load_boston() style.",
    long_description_content_type="text/markdown",
    url="https://github.com/dltpdn/boston",
    install_requires=['pandas'],
    packages=setuptools.find_packages(),
    package_data={'boston':['boston/resources/boston_house_prices.csv']},
    data_files=[('resources', ['boston/resources/boston_house_prices.csv'])],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
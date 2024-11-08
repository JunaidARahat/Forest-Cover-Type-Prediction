import setuptools

__version__ = "0.0.0"
AUTHOR_USER_NAME = "JunaidARahat"

setuptools.setup(
     version=__version__,
     name="Forest-Cover-Type-Prediction",
     author=AUTHOR_USER_NAME,
     package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
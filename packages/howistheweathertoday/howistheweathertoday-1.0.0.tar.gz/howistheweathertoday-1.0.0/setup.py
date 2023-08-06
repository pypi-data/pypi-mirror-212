from setuptools import setup
setup(
    name = "howistheweathertoday",
    packages = ["howistheweathertoday"],
    version="1.0.0",
    license="MIT",
    description="Weather forecast data",
    author="Mehmet Ali Soylu",
    author_email="mhmtsoylu1928@gmail.com",
    keywords=["weather","forecast","openweather"],
    install_requires=["requests"]
)
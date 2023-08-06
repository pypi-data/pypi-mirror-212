
import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "sidechannelattack",
    version = "0.0.2",
    author = "yangsu ",
    author_email = "1152036203@qq.com",
    description = "sidechannelattack",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # url="https://github.com/tqthooo2021/Create-Own-Python-Package",
    packages=setuptools.find_packages(),
    install_requires=['pandas','matplotlib','numpy','scipy','pandas_profiling','folium','seaborn'],
    # add any additional packages that needs to be installed along with SSAP package.

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
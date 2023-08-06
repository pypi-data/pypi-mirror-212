import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="kboxx",
    version="1.0.3",
    author="djsaber",
    author_email="479719615@qq.com",
    description="Implementation of pre-trained model based on Keras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djsaber/Keras-ViT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

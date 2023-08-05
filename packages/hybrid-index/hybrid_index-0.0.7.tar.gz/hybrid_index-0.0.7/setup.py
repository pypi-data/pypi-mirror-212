from setuptools import find_packages, setup

with open("hybrid/README.md", "r") as f:
    long_description = f.read()

setup(
    name="hybrid_index",
    version="0.0.7",
    description="Easy to use hybrid index for semantic + keyword search",
    package_dir={"": "hybrid"},
    packages=find_packages(where="hybrid"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gigagiova/hybrid-index",
    author="Giovanni del Gallo",
    author_email="giovanni@livesey.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      "attrs",
      "charset-normalizer",
      "click",
      "distlib",
      "faiss-gpu",
      "filelock",
      "frozenlist",
      "idna",
      "multidict",
      "nltk",
      "numpy",
      "openai",
      "platformdirs",
      "regex",
      "requests",
      "urllib3",
      "yarl",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_jsheet",
    version="0.2.1.1a",
    author="shadMod",
    author_email="support@shadmod.it",
    description="A little tool to render a simple excel sheet in webpage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadMod/django-jsheet",
    project_urls={
        "Bug Tracker": "https://github.com/shadMod/django-jsheet/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["django_jsheet"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={
        "assets": ["assets/index.js"],
    },
    python_requires=">=3.7"
)

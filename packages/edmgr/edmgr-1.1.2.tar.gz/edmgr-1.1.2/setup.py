from pathlib import Path
from setuptools import setup, find_packages

this_dir = Path(__file__).parent.resolve()
readme = (this_dir / "README.md").read_text(encoding="utf-8")

about: dict = {}
exec((this_dir / "edmgr" / "__version__.py").read_text(encoding="utf-8"), about)

setup(
    name="edmgr",
    version=about["__version__"],
    description="Entitlements and Download Manager",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    maintainer="Arm Ltd.",
    author="Digital Delivery",
    author_email="digital-delivery@arm.com",
    packages=find_packages(where=this_dir, exclude=["tests"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "click~=8.1",
        "cryptography>=3.4",
        "msal~=1.18",
        "pyjwt~=2.4",
        "requests~=2.28",
        "tabulate~=0.8",
        "tqdm~=4.64",
    ],
    entry_points={
        "console_scripts": [
            "edmgr=edmgr.edmgrcli:main",
        ]
    },
)

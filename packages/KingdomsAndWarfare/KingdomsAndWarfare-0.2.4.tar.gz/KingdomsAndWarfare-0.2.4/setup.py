from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()  # force no build without readme

setup(
    name="KingdomsAndWarfare",
    version="0.2.4",
    description="Kingdoms, Units, Unit Traits all for MCDM's excellent expansion for D&D",
    packages=[
        "KingdomsAndWarfare.Traits",
        "KingdomsAndWarfare.Units",
        "KingdomsAndWarfare.Kingdoms",
    ],
    python_requires=">=3.11",
    project_urls={"Source": "https://github.com/bleehu/PyMCDMKingdomsAndWarfare"},
)

from setuptools import setup

setup(
    name="mi_libreria",
    version="0.3",
    py_modules=["mi_libreria"],
    entry_points={
        "console_scripts": [
            "mi_libreria = mi_libreria.__main__:main"
        ]
    }
)

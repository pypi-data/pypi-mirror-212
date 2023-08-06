from setuptools import setup

def get_long_description(path):
    """Opens and fetches text of long descrition file."""
    with open(path, 'r') as f:
        text = f.read()
    return text

setup(
    name='CTkToolTip',
    version='0.4',
    description="Customtkinter Tooltip widget",
    license="Creative Commons Zero v1.0 Universal",
    readme = "README.md",
    long_description = get_long_description('README.md'),
    long_description_content_type="text/markdown",
    author='Akash Bora',
    url="https://github.com/Akascape/CTkToolTip",
    classifiers=[
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords=['customtkinter', 'tooltips', 'popup', 'widgets', 'tkinter-widgets', 'tooltip popup', 'floating window'],
    packages=["CTkToolTip"],
    python_requires='>=3.6',
)

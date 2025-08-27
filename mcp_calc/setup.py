from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="pycalc-sse",
    version="1.0.0",
    author="FastMCP",
    author_email="",
    description="一个基于 FastMCP 框架的简单计算器服务，通过 Server-Sent Events (SSE) 方式暴露 HTTP 服务",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pycalc-sse",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pycalc-sse=mcp_calc.src.server_sse:main',
        ],
    },
)
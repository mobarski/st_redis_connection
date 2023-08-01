import setuptools

VERSION = "0.1.1"

NAME = "st_redis_connection"

INSTALL_REQUIRES = [
	"redis"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Streamlit Connection for Redis.",
    url="https://github.com/mobarski/st_redis_connection",
    project_urls={
        "Source Code": "https://github.com/mobarski/st_redis_connection",
    },
    author="Maciej Obarski",
    author_email="mobarski@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["st_redis_connection"]
)


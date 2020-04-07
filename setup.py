from setuptools import setup, find_packages


def read_file(filename):
    with open(filename) as f:
        return f.read()


setup(
    python_requires="~=3.8",
    name="shopping-cart-service",
    version=read_file("cart_api/VERSION").strip(),
    description="Learning Python by building a shopping cart service.",
    long_description=read_file("README.md"),
    url="https://github.com/tjmaynes/learning-python",
    author="TJ Maynes",
    author_email="tj@tjmaynes.com",
    packages=find_packages(exclude=["*tests"]),
    package_data={"shopping_cart_service": ["URL", "VERSION", "*.txt", "*.yml", "*.template", "**/*.sh", "*.ini", "bin/**/*"]},
    include_package_data=True,
    setup_requires=[
        'wheel==0.34.2'
    ],
    install_requires=[
        'flask==1.1.1',
        'python-either@git+https://git@github.com/tjmaynes/python-either.git@0.0.1',
        'psycopg2-binary==2.8.5'
    ],
    extras_require={
        'dev': [
            'pylint==2.4.4'
        ]
    },
    entry_points={
        "console_scripts": [
            "shopping_cart_service=cart_api.api:main",
        ],
    },
)
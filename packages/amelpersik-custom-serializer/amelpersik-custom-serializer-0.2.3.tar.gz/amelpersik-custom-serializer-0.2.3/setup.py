from setuptools import setup

setup(
    name='amelpersik-custom-serializer',
    version='0.2.3',
    packages=[
        "lab3.serializer.src"
    ],
    entry_points={
        'console_scripts': [
            "custom-serialize = lab3.serializer.custom:main"
        ]
    },
    license='MIT',
    author='amelpersik',
    author_email='st.dasha.st@gmail.com',
    description='Python JSON and XML serializer',
)

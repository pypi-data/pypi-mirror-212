from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='spark-llm',
    version='0.1.1',
    url='https://github.com/gengliangwang/spark-llm',
    author='Gengliang Wang',
    author_email='gengliang@apache.org',
    description='LLM assistant for the development of Spark applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tiktoken',
        'beautifulsoup4',
        'langchain',
        'pyspark',
    ],
    python_requires='>=3.7', # Example, replace with your required python version
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)

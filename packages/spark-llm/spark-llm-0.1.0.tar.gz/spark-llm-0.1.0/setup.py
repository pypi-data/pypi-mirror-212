from setuptools import setup, find_packages

setup(
    name='spark-llm',
    version='0.1.0',
    url='https://github.com/gengliangwang/spark-llm',
    author='Gengliang Wang',
    author_email='gengliang@apache.org',
    description='LLM assistant for the development of Spark applications',
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

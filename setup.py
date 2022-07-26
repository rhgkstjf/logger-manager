import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
	name='rhgkstjf_logger_manager',
	version='1.0.0',
	description='python simple logger manager',
	author='rhgkstjf',
	author_email='rhgkstjf@gmail.com',
	url="https://github.com/rhgkstjf/logger-manager",
	install_requires = ["fluent-logger",
						"requests",
						"urllib3"],
	packages=setuptools.find_packages(),
	long_description=long_description,
    long_description_content_type="text/markdown",
	classifiers      = [
		'Programming Language :: Python :: 3'
	],
	python_requires='>=3.6'
)
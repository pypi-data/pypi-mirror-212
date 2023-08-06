# ezlab

ezlab is a Python package that helps you manage files in Google Colab notebooks. It provides three functions:

- `start_work()`: This function uploads files or a zip file from your local machine (and extracts the zip file is the user wants) in the current working directory.
- `finish_work(output_zip_file_name)`: This function zips all the files in the current working directory and downloads the zip file with the given name.
- `clear_directory()`: This function deletes all the files and folders in the current working directory, effectively resetting the working directory.

## Installation

You can install ezlab using pip:

` !pip install ezlab `


## Usage

To use ezlab, you need to import it in your notebook:

`import ezlab as ec`


Then you can call any of the functions as needed. For example, to upload and extract "my_project.zip" in your current directory, you can use:

`ec.start_work("my_project.zip")`


To zip and download all the files in your current directory as "my_project.zip", you can use:

`ec.finish_work("my_project.zip")`


To delete all the files and folders in your current directory, you can use:

`ec.clear_directory()`


## License

This package is licensed under the MIT License. See the __LICENSE.txt__ file for more details.
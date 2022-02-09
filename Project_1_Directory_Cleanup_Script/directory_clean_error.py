import os
import argparse

# Pre-requisite
# prepare the test_directory. Run the test_directory.sh bash script using
# chmod +x test_directory.sh
# ./test_directory.sh


# Step-0: Setting the argument parser
# Create an ArgumentParser object named 'parser'
# The ArgumentParser object will hold all the information necessary to parse the command line into Python data types.
parser = argparse.ArgumentParser(
    description="Clean up directory and put files into according folders"
)

# Fill the ArgumentParser object i.e. 'parser' with information about program arguments using parser.add_argument() method
# Generally, these calls tell the ArgumentParser how to take the strings on the command line and turn them into objects
# This information is stored and used when parse_args() is called.
parser.add_argument(
    "--path",
    type=str,
    default=".",
    help="Directory path of the (to be) cleaned up directory"
)

# ArgumentParser parses arguments through the parse_args() methods.
# This will inspect the command line, convert each argument to the appropriate type and then invoke the appropriate action.
# In mose cases, it means a simple Namespace object will be built up from attributes parsed out of the command line.
args = parser.parse_args()
path = args.path
print(f"Cleaning up directory {path}")

'''
Test the argument parser
---------------------------
> python3 directory_clean_error.py -h
> python3 directory_clean_error.py --path ./test_directory
'''

# Step-1: Get all files from the given directory
dir_content = os.listdir(path)                                                                # this will return a list of all files and folders in the directory i.e. [image1.png, ...]
path_dir_content = [os.path.join(path, doc) for doc in dir_content]                           # return a list in the format [ ./test_directory/image1.png, ...]
docs = [doc for doc in path_dir_content if os.path.isfile(doc)]                               # return a list of all files
folders = [folder for folder in path_dir_content if os.path.isdir(folder)]                    # return a list of all folders i.e. ['./test_directory/png', './test_directory/jpg', './test_directory/pdf', './test_directory/txt']
moved = 0

print(f"Cleaning up {len(docs)} of {len(dir_content)} elements")                              # i.e. Cleaning up 40 of 44 elements

# Step-2: Rename the filepath of each file and create folder with respective file extension and move the file to the respective folder.
# Take care of the current script which is may be running in your current path
# Take care of the hidden_files which doesnt require to be moved
for doc in docs:
    # 2.1 separate name from file extension
    full_doc_path, filetype = os.path.splitext(doc)                                           # returns a tuple. os.path.splitext("./test/xyz.txt") -> ('./test/xyz', '.txt')
    doc_path = os.path.dirname(full_doc_path)                                                 # os.path.dirname("./test/xyz") -> ./test
    doc_name = os.path.basename(full_doc_path)                                                # os.path.basename("./test/xyz") -> xyz

    # 2.5 try to handle the hidden file exists, else it will raise an error
    if doc_name == "directory_clean_error" or doc_name.startswith("."):
        print(f"--> [{doc_name}] is either a current script or hidden file. Escaping...")
        continue

    # 2.2 get the subfolder name and create the folder if not exist
    subfolder_path = os.path.join(path, filetype[1:].lower())                                 # path-> ./text; filetype=.txt; filetype[1:]-> txt;
                                                                                              # returns, ./text/txt and create the subfolder txt; similarly for pdf, jpg, png etc
    if subfolder_path not in folders:
        try:                                                                                  # Make sure you have try..except exceptionHandler is place
            os.mkdir(subfolder_path)                                                          # create the subfolder
            folders.append(subfolder_path)                                                    # append the folder list with the newly created subfolder
            print(f"Folder {subfolder_path} is created.")
        except FileExistsError as err:
            print(f"Folder {subfolder_path}{doc_name} already exists")                        # example; Folder /home/jarotball/Downloads/pypdf_demo-58ad283e-eb61-4767-af1f-e8b3e5e8296a already exists


    # 2.3 get the new folder path and move the file
    new_doc_path = os.path.join(subfolder_path,doc_name)+filetype                             # subfolder_path-> ./test/txt; doc_name-> file1; filetype-> .txt
                                                                                              # returns, ./test/txt/file1.txt
    # 2.4 Now, actually move the file to their respective folder
    if new_doc_path != doc:
        os.rename(doc, new_doc_path)                                                              # os.rename("./test/file.txt", "./test/txt/file1.txt")
        print(f"Moved file {doc} to {new_doc_path}")                                              # example, Moved file ./test_directory/pfile3.pdf to ./test_directory/pdf/pfile3.pdf
        moved += 1
    # else:
    #     print(f"{new_doc_path}")

print(f"Moved file {moved} of {len(docs)} files")
#print(folders)

'''
Use Cases:
----------
> python3 directory_clean_error.py
> python3 directory_clean_error.py --path ./test_directory
> python3 directory_clean_error.py --path /home/jarotball/Downloads/
'''






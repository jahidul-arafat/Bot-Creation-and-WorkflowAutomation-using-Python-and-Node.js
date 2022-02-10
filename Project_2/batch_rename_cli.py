import os, sys
import argparse

'''
Cli Syntax that we will develop
> python3 batch_rename_cli.py <searchText:Mandatory> <replaceText:Mandatory> --filetype <.txt|.pdf|.png> --path <path/to/your/directory>
'''
# Step-0.0: Setting up the argparser
parser = argparse.ArgumentParser(description="Batch rename file in directory")

# Mandatory Arguments (2x) | Must not be starting with --
# Mandatory Argument: <search>
parser.add_argument(
    "search",
    type=str,
    help="To be replaced text"
)

# Mandatory Argument: <replace>
parser.add_argument(
    "replace",
    type=str,
    help="Text to use for replacement"
)

# Optional Arguments (2x)| Must be starting with --
# Optional Argument: --filetype
parser.add_argument(
    "--filetype",
    type=str,
    default=None,
    help="Only files with the given type will be renamed"
)

# Optional Argument: --path
parser.add_argument(
    "--path",
    type=str,
    default=".",  # Current Directory
    help="Directory path that contains the to be renamed files"
)

# get all the arguments
args = parser.parse_args()                                                      # python3 batch_rename_cli.py file doc --filetype .py --path ./test_directory
print(args)                                                                     # Namespace(filetype='.py', path='./test_directory', replace='doc', search='file')



# Step-0.1: A first layer confirmation to make sure you accidentally dont clear any directory
user_response = input("Do you want to continue (Y/N)").lower()
if user_response == "n":
    sys.exit(0)

# Step-1: Fetch the "search", "replace", "filetype" and "path" from argparser
search = args.search
replace = args.replace
type_filter = args.filetype
path = args.path

print(f"Renaming files at path {path}")

# Step-2: Rename Operation
# 2.1 get all files from current directory or path you passed as argument
dir_content = os.listdir(path)                                                 # ['pimage8.png', 'file7.txt',...]. Only returns the file name, not the leading path of the file
path_dir_content = [os.path.join(path,doc) for doc in dir_content]             # [./path/leading/to/your/file.txt,...]
docs = [doc for doc in path_dir_content if os.path.isfile(doc)]                # get the list of all files, escape the folders
rename_count = 0
# print(dir_content)
# print(path_dir_content)
# print(docs)

print(f"{len(docs)} of {len(dir_content)} elements are files")

# 2.2 go through all the files and check if they match the <search> pattern
for doc in docs:
    # 2.2.1 separate the file name from file extension
    full_doc_path, filetype = os.path.splitext(doc)                             # os.path.splitext("./path/leading/to/your/file.txt") -> ('./path/leading/to/your/file', '.txt')
    doc_path = os.path.dirname(full_doc_path)                                   # ./path/leading/to/your/
    doc_name = os.path.basename(full_doc_path)                                  # fileName without any extension

    # 2.2.2 filter for files with right extension
    # Scenario-1: With filetype explicitly mentioned in cli command
    # > python3 batch_rename_cli.py <searchText:Mandatory> <replaceText:Mandatory> --filetype <.txt|.pdf|.png> --path <path/to/your/directory>

    # Scenario-2: Without filetype mentioned in cli command, in this case <type_filer is None>
    # > python3 batch_rename_cli.py <searchText:Mandatory> <replaceText:Mandatory> --path <path/to/your/directory>
    if filetype == type_filter or type_filter is None:
        # A. check if <search> text is in doc_name, then replace with <replace> text
        if search in doc_name:
            # replace with given text
            new_doc_name = doc_name.replace(search, replace)
            new_doc_path = os.path.join(doc_path, new_doc_name) + filetype
            #os.rename(doc, new_doc_path)                                          # Actual rename is executed here and file is successfully renamed
            rename_count += 1

            print(f"Renamed file {doc} to {new_doc_path}")

print(f"Renamed {rename_count} of {len(docs)} files")


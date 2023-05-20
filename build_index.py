
import lib__embedded_context

# Test the build_index(folder_path) function
# Path to index : files/

folder_path = '<path to the folder containing the files to index>'
# ex: folder_path = 'files/'
# careful : only txt files.

# build the index and save it in a csv file in the folder_path
lib__embedded_context.build_index(folder_path)


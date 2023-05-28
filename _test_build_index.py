
import lib__embedded_context
import sendmail

# Test the build_index(folder_path) function
# Path to index : files/

# get the zip file from http post request



# generate a folder name with a timestamp


# unzip the file in the folder



#folder_path = '<path to the folder containing the files to index>'
folder_path = 'datas/scenarioslogement/'
# careful : only txt files.

# build the index and save it in a csv file in the folder_path
brain_id = lib__embedded_context.build_index(folder_path)
print(brain_id)
#sendmail.mailfile('michel@brightness.fr', None, brain_id)

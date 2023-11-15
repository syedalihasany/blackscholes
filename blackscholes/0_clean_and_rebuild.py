import shutil
import os

def delete_directory_contents(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

directory_to_clear = "./build" 
delete_directory_contents(directory_to_clear)
directory_to_clear = "./compiled_binary" 
delete_directory_contents(directory_to_clear)




os.chdir(r"./build")
cmd1 = 'cmake ..'
os.system(cmd1)
cmd2 = 'make'
os.system(cmd2)
cmd3 = 'mv ./blackscholes ../compiled_binary/blackscholes'
os.system(cmd3)
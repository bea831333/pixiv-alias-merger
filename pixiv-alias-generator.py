import os,sys,re, string
import shutil
import datetime

def create_alias(path, name):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(name+"\n")
    print("Created alias in ", path)

def merge_alias_files(source_file_path, dest_file_path):
    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_lines = source_file.read().splitlines()
    with open(dest_file_path, 'r', encoding='utf-8') as dest_file:
        dest_lines = dest_file.read().splitlines()
        
    with open(dest_file_path, 'a', encoding='utf-8') as dest_file:
        for source_line in source_lines:
            if source_line not in dest_lines:
                dest_file.write(source_line + "\n")
    
    os.remove(source_file_path)
    print("Merged aliases ", source_file_path, " to ", dest_file_path) 

def move_files(source_dir, target_dir):
    filenames = os.listdir(source_dir)
    for filename in filenames:
        source_file = os.path.join(source_dir, filename)
        if os.path.exists(os.path.join(target_dir, filename)):
            name, ext = os.path.splitext(filename)
            file_date = datetime.datetime.fromtimestamp(os.path.getctime(source_file))
            datestring = file_date.strftime("%Y%m%d_%H%M%S")
            new_filename = "{name}_{datestring}{ext}".format(name=name, datestring=datestring, ext=ext)
            shutil.copy(source_file, os.path.join(target_dir, new_filename))
            os.remove(source_file)
        else:
            shutil.move(os.path.join(source_dir, filename), target_dir)
    os.rmdir(source_dir)

if __name__ == "__main__":
    pixiv_folder_path = sys.argv[1]
    pixiv_dict = {}
    pixiv_path_dict = {}
    _alias = "alias.txt"
  
    for item in os.listdir(pixiv_folder_path):
        path = os.path.join(pixiv_folder_path, item)
        number = item.split('(')[-1][:-1]
        name = item[0:item.rfind('(')].strip()
        name = re.sub(r'[^\w_. -]', '_', name)
        if not name:
            name = number
        
        child_alias_file = os.path.join(path, _alias)
        if not os.path.isfile(child_alias_file):
            create_alias(child_alias_file, item)
        
        if number not in pixiv_dict:
            pixiv_dict[number] = name
            pixiv_path_dict[number] = item
        else:
            parent_path = os.path.join(pixiv_folder_path, pixiv_path_dict[number])
            parent_alias_file = os.path.join(parent_path, _alias)
            
            merge_alias_files(child_alias_file, parent_alias_file)
            move_files(path, parent_path)
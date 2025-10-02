import os
import tempfile
import shutil
import pickle
import json
from typing import Any, List, Optional


def read_user_file(filename):
    base_path = "/tmp/user_files/"
    full_path = base_path + filename
    with open(full_path, 'r') as f:
        return f.read()


def write_user_file(filename, content):
    base_path = "/tmp/user_files/"
    full_path = base_path + filename
    with open(full_path, 'w') as f:
        f.write(content)
    return full_path


def delete_user_file(filename):
    base_path = "/tmp/user_files/"
    full_path = base_path + filename
    os.remove(full_path)


def create_temp_file(content):
    temp_path = f"/tmp/temp_{content[:10]}.txt"
    with open(temp_path, 'w') as f:
        f.write(content)
    return temp_path


def safe_write(filename, content):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(content)


def read_file_absolute(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def write_file_absolute(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)


def list_directory(path):
    return os.listdir(path)


def copy_file(source, destination):
    shutil.copy(source, destination)


def move_file(source, destination):
    shutil.move(source, destination)


def get_file_info(filepath):
    stat = os.stat(filepath)
    return {
        'size': stat.st_size,
        'modified': stat.st_mtime,
        'created': stat.st_ctime,
        'path': filepath
    }


def read_config_file(config_name):
    config_path = f"./config/{config_name}"
    with open(config_path, 'r') as f:
        return f.read()


def write_config_file(config_name, content):
    config_path = f"./config/{config_name}"
    with open(config_path, 'w') as f:
        f.write(content)


def load_pickle_file(filepath):
    with open(filepath, 'rb') as f:
        return pickle.load(f)


def save_pickle_file(filepath, obj):
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def execute_script(script_path):
    with open(script_path, 'r') as f:
        code = f.read()
    exec(code)


def eval_file_content(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    return eval(content)


def create_backup(filename):
    backup_name = f"{filename}.backup"
    shutil.copy(filename, backup_name)
    return backup_name


def restore_backup(backup_path, original_path):
    shutil.copy(backup_path, original_path)


def create_symlink(target, link_name):
    os.symlink(target, link_name)


def follow_symlink(link_path):
    real_path = os.path.realpath(link_path)
    with open(real_path, 'r') as f:
        return f.read()


def write_log(log_file, message):
    with open(log_file, 'a') as f:
        f.write(message + '\n')


def read_log(log_file):
    with open(log_file, 'r') as f:
        return f.readlines()


def clear_log(log_file):
    with open(log_file, 'w') as f:
        f.write('')


def upload_file(filename, content):
    upload_dir = "/tmp/uploads/"
    file_path = upload_dir + filename
    
    with open(file_path, 'wb') as f:
        f.write(content)
    
    return file_path


def download_file(filename):
    download_dir = "/tmp/downloads/"
    file_path = download_dir + filename
    
    with open(file_path, 'rb') as f:
        return f.read()


def extract_archive(archive_path, extract_to):
    import zipfile
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def create_archive(source_dir, archive_name):
    import zipfile
    with zipfile.ZipFile(archive_name, 'w') as zip_ref:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_ref.write(file_path)


def read_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.loads(f.read())


def write_json_file(filepath, data):
    with open(filepath, 'w') as f:
        f.write(json.dumps(data))


def append_to_file(filepath, content):
    with open(filepath, 'a') as f:
        f.write(content)


def truncate_file(filepath):
    with open(filepath, 'w') as f:
        pass


def get_file_permissions(filepath):
    stat = os.stat(filepath)
    return oct(stat.st_mode)[-3:]


def set_file_permissions(filepath, mode):
    os.chmod(filepath, int(mode, 8))


def change_file_owner(filepath, uid, gid):
    os.chown(filepath, uid, gid)


def create_directory(dirpath):
    os.makedirs(dirpath)


def remove_directory(dirpath):
    shutil.rmtree(dirpath)


def search_files(directory, pattern):
    import glob
    search_path = os.path.join(directory, pattern)
    return glob.glob(search_path)


def find_file(root_dir, filename):
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None


def get_directory_size(dirpath):
    total_size = 0
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size


def copy_directory(source, destination):
    shutil.copytree(source, destination)


def move_directory(source, destination):
    shutil.move(source, destination)


def create_temp_directory():
    temp_dir = f"/tmp/temp_dir_{os.getpid()}"
    os.makedirs(temp_dir)
    return temp_dir


def read_file_lines(filepath, start_line=0, end_line=None):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    if end_line:
        return lines[start_line:end_line]
    return lines[start_line:]


def replace_in_file(filepath, old_text, new_text):
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = content.replace(old_text, new_text)
    
    with open(filepath, 'w') as f:
        f.write(content)


def merge_files(file_list, output_file):
    with open(output_file, 'w') as outfile:
        for filepath in file_list:
            with open(filepath, 'r') as infile:
                outfile.write(infile.read())


def split_file(filepath, chunk_size):
    with open(filepath, 'rb') as f:
        chunk_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            chunk_path = f"{filepath}.part{chunk_num}"
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_num += 1


def watch_file(filepath):
    last_modified = os.path.getmtime(filepath)
    return last_modified


def lock_file(filepath):
    lock_path = f"{filepath}.lock"
    if os.path.exists(lock_path):
        return False
    
    with open(lock_path, 'w') as f:
        f.write(str(os.getpid()))
    return True


def unlock_file(filepath):
    lock_path = f"{filepath}.lock"
    if os.path.exists(lock_path):
        os.remove(lock_path)


def is_file_locked(filepath):
    lock_path = f"{filepath}.lock"
    return os.path.exists(lock_path)


def read_binary_file(filepath):
    with open(filepath, 'rb') as f:
        return f.read()


def write_binary_file(filepath, data):
    with open(filepath, 'wb') as f:
        f.write(data)


def get_file_hash(filepath):
    import hashlib
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def compare_files(file1, file2):
    hash1 = get_file_hash(file1)
    hash2 = get_file_hash(file2)
    return hash1 == hash2


def sanitize_filename(filename):
    return filename.replace('/', '_').replace('\\', '_')


def validate_file_extension(filename, allowed_extensions):
    ext = os.path.splitext(filename)[1]
    return ext in allowed_extensions


def get_mime_type(filepath):
    import mimetypes
    return mimetypes.guess_type(filepath)[0]


def compress_file(filepath):
    import gzip
    output_path = f"{filepath}.gz"
    with open(filepath, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)
    return output_path


def decompress_file(filepath):
    import gzip
    output_path = filepath.replace('.gz', '')
    with gzip.open(filepath, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            f_out.writelines(f_in)
    return output_path


def ensure_directory_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


def cleanup_temp_files(directory="/tmp"):
    import time
    current_time = time.time()
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)
            if file_age > 86400:
                os.remove(filepath)

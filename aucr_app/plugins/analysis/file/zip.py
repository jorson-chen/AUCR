"""Zip file parsing"""
# coding=utf-8
import os
import hashlib
import subprocess
import fleep
from zipfile import ZipFile


def decrypt_zip_file_map(encrypted_zip, encrypted_file_password):
    """Return decrypted zip file map bytes object."""
    encrypted_zip_file = ZipFile(encrypted_zip)
    for file in encrypted_zip_file.namelist():
        if encrypted_zip_file.getinfo(file).file_size < 1024 * 1024:
            file_map = encrypted_zip_file.read(file, pwd=encrypted_file_password.encode('utf-8'))
            return file_map


def write_file_map(file_object, file_path):
    """Return md5 hash of a compressed file."""
    file_md5_hash = hashlib.md5()
    if type(file_object) is not bytes:
        file_map = file_object.read()
        info = fleep.get(file_object.read(128))
    else:
        file_map = file_object
        info = fleep.get(file_object[:128])
    file_md5_hash.update(file_map)
    file_md5_hash: object = file_md5_hash.hexdigest()
    full_file_path_and_name = str(file_path + "/" + file_md5_hash)
    with open(full_file_path_and_name, 'wb') as open_file_object:
        open_file_object.write(file_map)
    file_dict = {"md5_hash": file_md5_hash, "file_info": info}
    return file_dict


def get_file_hash(file_name):
    file_md5_hash = hashlib.md5()
    file_md5_hash.update(file_name.read())
    file_hash: object = file_md5_hash.hexdigest()
    with open(str(file_hash), 'wb') as read_file:
        read_file.write(file_name.read())
    return file_hash


def encrypt_zip_file(password, zip_file, items_to_encrypt):
    """Subprocess call to encrypt zip file."""
    subprocess.call(['7z', 'a', str("-p" + password), '-y', str(os.environ.get('TMP_FILE_FOLDER') + zip_file)] +
                    items_to_encrypt)

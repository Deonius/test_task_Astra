import os
import argparse
import hashlib
import logging
import subprocess


# временный файл
def create_iso_file(size):
    iso_file = "/tmp/iso_file"
    with open(iso_file, "wb") as f:
        f.write(os.urandom(size))
    return iso_file


def calculate_md5_sum(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()


def fill_external_device(device_name, fill_percent):
    device_size = os.statvfs(device_name).f_frsize * os.statvfs(device_name).f_blocks
    fill_size = int(device_size * fill_percent / 100)
    iso_files = []
    written_size = 0
    while written_size < fill_size:
        iso_size = min(fill_size - written_size, int(1e9))
        iso_file = create_iso_file(iso_size)
        md5_sum = calculate_md5_sum(iso_file)
        subprocess.run(["cp", iso_file, device_name])
        iso_files.append((os.path.basename(iso_file), iso_size, md5_sum))
        os.remove(iso_file)
        written_size += iso_size
    total_size = os.statvfs(device_name).f_frsize * os.statvfs(device_name).f_blocks
    used_size = os.stat(device_name).st_size
    free_size = total_size - used_size
    logging.info(f"External device {device_name} is filled with {fill_percent}% of data.")
    logging.info(f"Total size: {total_size}, used size: {used_size}, free size: {free_size}")

    for iso_file in iso_files:
        logging.info(f"iso_name: {iso_file[0]}, iso_size: {iso_file[1]}, md5sum: {iso_file[2]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("device_name", help="Name of the external device")
    parser.add_argument("fill_percent", type=float, help="Percentage of the device to fill")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

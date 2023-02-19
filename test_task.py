# Задание  - Написать скрипт на Python
# Скрипт должен заполнить внешнее устройство сгенерированными iso файлами (например с помощью genisoimage) разного размера на указанную процентную величину
# и посчитать для каждого файла md5 сумму. Скрипт должен содержать логер, для документирования своих действий. Входные данный передаются с помощью ключей как во всех Posix системах.
# Окружение:
#  • Debian или Astra Linux
# Входные данные:
#  • имя внешнего устройства (флешки, vdi и т.д,)
#  • величина заполнения в процентах
# Выходные данные:
#  • вывести общий объем внешнего устройства
#  • вывести список созданных iso файлов вида: iso_name <> iso_size <> md5sum

import argparse
import hashlib
import logging
import os
import subprocess

logging.basicConfig(filename='logger.log', level=logging.INFO)


def fill_external_device(device_name: str, fill_value: int):
    total_size = os.statvfs(device_name).f_frsize * os.statvfs(device_name).f_blocks
    used_size = os.stat(device_name).st_size
    available_size = total_size - used_size
    fill_size = int(available_size * fill_value / 100)
    logging.info(f'Total size of {device_name} : {total_size / (1024 * 1024)} MB')
    logging.info(f'Available size of {device_name}: {available_size / (1024 * 1024)} MB')
    logging.info(f'Filling {fill_value}% of {device_name} ({fill_size / (1024 * 1024)} MB)')
    remaining_size = fill_size
    generated_isos = []
    iso_index = 1
    while remaining_size > 0:
        iso_name = f'iso{iso_index}.iso'
        iso_size = min(remaining_size, 1024 * 1024 * 100)
        cmd = f'genisoimage -quiet -o {iso_name} -r -J /dev'
        cmd2 = f'mv {iso_name} /home/astra/Desktop/tests/generated_iso'  # move to
        subprocess.run(cmd.split(' '), check=True)
        md5sum = hashlib.md5(open(iso_name, 'rb').read()).hexdigest()
        subprocess.run(cmd2.split(' '), check=True)
        generated_isos.append((iso_name, iso_size, md5sum))
        remaining_size -= iso_size
        iso_index += 1
    logging.info('Generated ISO files:')
    for iso_name, iso_size, md5sum in generated_isos:
        logging.info(f'{iso_name} <> {iso_size / (1024 * 1024)} MB <> {md5sum}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('device_name', type=str, help='Name of the external device')
    parser.add_argument('fill_value', type=float, help='Percentage of the device to fill')
    args = parser.parse_args()
    fill_external_device(args.device_name, args.fill_value)


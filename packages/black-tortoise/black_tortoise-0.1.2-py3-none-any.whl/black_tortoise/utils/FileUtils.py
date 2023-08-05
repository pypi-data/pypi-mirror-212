#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import shutil
from typing import Optional

"""
@auther: Lambert
@file: FileUtils.py
@time: 2023/6/2 21:12
"""


class FileUtils(object):
    """
    文件工具类。
    """

    @staticmethod
    def create_file(file_path: str) -> Optional[bool]:
        """
        创建新文件。

        :param file_path: 要创建的文件的路径
        :return: True 表示成功创建
        :raises IOError: 如果创建文件时发生错误，抛出此异常
        """
        try:
            open(file_path, 'a').close()
            return True
        except Exception as e:
            raise IOError(f"Error: Failed to create file {file_path}. {str(e)}")

    @staticmethod
    def copy_file(src_file_path: str, dst_file_path: str) -> Optional[bool]:
        """
        复制文件。

        :param src_file_path: 原文件路径
        :param dst_file_path: 目标文件路径
        :return: True 表示成功复制
        :raises IOError: 如果复制文件时发生错误，抛出此异常
        """
        try:
            shutil.copy(src_file_path, dst_file_path)
            return True
        except Exception as e:
            raise IOError(f"Error: Failed to copy file {src_file_path} to {dst_file_path}. {str(e)}")

    # 之前的 delete_file 和 rename_file 方法

    @staticmethod
    def get_file_size(file_path: str) -> Optional[int]:
        """
        获取文件大小。

        :param file_path: 文件路径
        :return: 文件大小（字节）
        :raises FileNotFoundError: 如果文件不存在，抛出此异常
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Error: File {file_path} not found.")

        return os.path.getsize(file_path)

    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        """
        读取文件内容。

        :param file_path: 文件路径
        :return: 文件内容
        :raises FileNotFoundError: 如果文件不存在，抛出此异常
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Error: File {file_path} not found.")

        with open(file_path, 'r') as file:
            content = file.read()
        return content

    @staticmethod
    def write_file(file_path: str, content: str) -> Optional[bool]:
        """
        写入文件内容。

        :param file_path: 文件路径
        :param content: 要写入的内容
        :return: True 表示成功写入
        :raises IOError: 如果写入文件时发生错误，抛出此异常
        """
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return True
        except Exception as e:
            raise IOError(f"Error: Failed to write to file {file_path}. {str(e)}")

    @staticmethod
    def append_file(file_path: str, content: str) -> Optional[bool]:
        """
        在文件末尾添加内容。

        :param file_path: 文件路径
        :param content: 要添加的内容
        :return: True 表示成功添加
        :raises IOError: 如果添加内容时发生错误，抛出此异常
        """
        try:
            with open(file_path, 'a') as file:
                file.write(content)
            return True
        except Exception as e:
            raise IOError(f"Error: Failed to append to file {file_path}. {str(e)}")

    # 新增删除文件方法，如果存在就删除
    @staticmethod
    def delete_file(file_path: str) -> Optional[bool]:
        """
        删除文件。

        :param file_path: 文件路径
        :return: True 表示成功删除，False 表示文件不存在
        :raises OSError: 如果删除文件时发生错误，抛出此异常
        """
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                return True
            else:
                return False
        except Exception as e:
            raise OSError(f"Error: Failed to delete file {file_path}. {str(e)}") from e


if __name__ == '__main__':
    pass

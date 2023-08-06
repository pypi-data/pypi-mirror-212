#! env python3
# -*- coding:utf-8 -*-
"""
Password Manager
"""
import json
import os
import pyperclip
import sys
from jax_tools.encrypt import AESCipher
from jax_tools.utils.settings import JAX_DATA_DIR


class PasswordManager(object):
    """
    Password Manager
    """
    # Define pam data file
    data_file = os.path.join(JAX_DATA_DIR, '.pam.json')
    if os.path.exists(data_file):
        data_list = json.loads(open(data_file, 'r').read())
    else:
        data_list = list()

    # Define string
    NAME = 'name'
    USERNAME = 'username'
    PASSWORD = 'password'
    DUPLICATE_ACCOUNT = u'您输入的账号名在系统中已存在，请修改账号名进行区分'
    ACCOUNT_CREATED = u'账号{}已创建成功'
    ACCOUNT_DELETED = u'账号{}已删除成功'
    NUM_OF_ACCOUNT = u'第{0}个账号信息: {1}'
    ACCOUNT_NOT_FOUND = u'账号{}没有找到格，如果您输入的账号信息含空格，请将完整的账号引号"包裹起来'

    @classmethod
    def get_password(cls, search_str=None):
        """
        Get Password
        Args:
            search_str: Search string

        Returns: password

        """
        over = False
        for encrypted_pw_info in cls.data_list:
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            name = pw_info.get(cls.NAME)
            if name == search_str:
                pyperclip.copy(pw_info.get(cls.PASSWORD))
                over = True
                break
        if not over:
            for encrypted_pw_info in cls.data_list:
                pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
                name = pw_info.get(cls.NAME)
                if name.__contains__(search_str):
                    pyperclip.copy(pw_info.get(cls.PASSWORD))
                    break

    @classmethod
    def print_account_list(cls):
        """
        Print account list
        Returns:

        """
        for encrypted_pw_info in cls.data_list:
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            name = pw_info.get(cls.NAME)
            username = pw_info.get(cls.USERNAME)
            data = {cls.NAME: name, cls.USERNAME: username, cls.PASSWORD: '********'}
            print(cls.NUM_OF_ACCOUNT.format(cls.data_list.index(encrypted_pw_info) + 1, data))

    @classmethod
    def delete_account(cls, name):
        """
        Delete account
        Args:
            name: Account name

        Returns:

        """
        for encrypted_pw_info in cls.data_list:
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            account_name = pw_info.get(cls.NAME)
            if name == account_name:
                cls.data_list.remove(encrypted_pw_info)
                # dump account list to json
                data_json = json.dumps(cls.data_list)
                # write to data file
                open(cls.data_file, 'w').write(data_json)
                # Print finally message
                print(cls.ACCOUNT_DELETED.format(name))
                return
        print(cls.ACCOUNT_NOT_FOUND.format(name))

    @classmethod
    def add_account(cls, name, username, password):
        """
        Add Account to data file
        Args:
            name: Account name
            username: Username
            password: Password

        Returns:

        """
        # Traverse encrypted account list
        for encrypted_pw_info in cls.data_list:
            # Get account information
            pw_info = json.loads(AESCipher().decrypt(encrypted_pw_info))
            account_name = pw_info.get(cls.NAME)
            # If new name is duplicate with exist name, return and print a message
            if name == account_name:
                print(cls.DUPLICATE_ACCOUNT)
                return
        # Define account information use a dict
        account_info = {cls.NAME: name, cls.USERNAME: username, cls.PASSWORD: password}
        # Define encrypted account information
        encrypted_account_info = AESCipher().encrypt(json.dumps(account_info))
        # Add new account to account list
        cls.data_list.append(encrypted_account_info)
        # dump account list to json
        data_json = json.dumps(cls.data_list)
        # write to data file
        open(cls.data_file, 'w').write(data_json)
        # Print finally message
        print(cls.ACCOUNT_CREATED.format(name))


if __name__ == '__main__':
    try:
        PasswordManager.get_password(sys.argv[1])
    except IndexError:
        pass

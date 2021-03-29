#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lex
# @Desc    :
"""

对SQLAlchemy的数据库常见异常的包装

"""

from sqlalchemy.exc import ProgrammingError


class GoodMessageDatabaseException(ProgrammingError):
    def __init__(self, programming_error: ProgrammingError):
        self.error_no = programming_error.orig.errno
        self.error_message = self.__wrapper_error_message(programming_error)
        self.orig = programming_error.orig

    def __wrapper_error_message(self, programming_error: ProgrammingError) -> str:
        error_message = 'Database error'
        if programming_error.orig.errno == 1049:
            # "Unknown database 'xxx'"
            error_message = '未找到对应的数据库'
        elif programming_error.orig.errno == 1064:
            # "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for
            # the right syntax to use near 'xxx' at line ..."
            error_message = 'SQL语句中存在语法错误'
        elif programming_error.orig.errno == 1146:
            # "Table 'xxx' doesn't exist"
            error_message = '对应的表不存在'
        else:
            error_message = programming_error.orig.msg
        return error_message

    def __get_friendly_error_message(self):
        return self.error_message

    @staticmethod
    def get_friendly_error_message(programming_error: ProgrammingError):
        return GoodMessageDatabaseException(programming_error).__get_friendly_error_message()

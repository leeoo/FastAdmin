#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lex
# @Desc    :
"""

"""
import datetime
from typing import Union, List, Optional
from pydantic import BaseModel, AnyHttpUrl, conint


class DatabaseConnectionInfoCreate(BaseModel):
    """
    新增数据库连接信息
    """
    # id: int
    connection_name: str
    database_type: str
    database_version: str
    host: str
    port: str
    database_name: str
    charset: str
    username: str
    password: str
    connection_url: str
    enabled: int = 1
    remark: str
    create_by: Optional[str]
    update_by: Optional[str]
    create_at: Optional[datetime.datetime]
    update_at: Optional[datetime.datetime]
    version: Optional[int] = 1
    valid: Optional[int] = 1


class DatabaseConnectionInfoUpdate(DatabaseConnectionInfoCreate):
    """
    更新数据库连接信息
    """
    id: Union[int, str]


class DatabaseConnectionInfoDel(BaseModel):
    """
    逻辑删除
    """
    ids: List[int]


class CategoryEnable(DatabaseConnectionInfoDel):
    """
    批量操作开启开关 继承 ids:List[int]
    """
    enabled: int


class DatabaseConnectionInfoSearch(BaseModel):
    """
    搜索数据库连接信息
    """
    keyword: str
    page: conint(ge=1) = 1
    page_size: conint(le=100) = 10

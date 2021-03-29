#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author  : Lex
# @Desc    :
"""
数据源 models

"""

from sqlalchemy import Column, Integer, BIGINT, VARCHAR, SmallInteger, TEXT
from api.db.base_class import Base, CommonBase, gen_uuid


class DatabaseConnectionInfo(CommonBase):
    """
    数据库连接信息表
    """
    __tablename__ = "database_connection_info"
    # id = Column(VARCHAR(128), default=gen_uuid, index=True, unique=True)
    connection_name = Column(VARCHAR(30), default='', index=True, comment="连接名称")
    database_type = Column(VARCHAR(20), default='MySQL', index=True, comment="数据库类型")
    database_version = Column(VARCHAR(50), default='', comment="数据库版本")
    host = Column(VARCHAR(100), default='', comment="主机名或IP")
    port = Column(VARCHAR(10), comment="端口")
    database_name = Column(VARCHAR(100), default='', index=True, comment="数据库名")
    charset = Column(VARCHAR(20), default='', comment="字符集: MySQL使用utf8mb4，其他数据库使用utf8")
    username = Column(VARCHAR(20), default='', comment="用户名")
    password = Column(VARCHAR(200), default='', index=True, comment="密码")
    connection_url = Column(VARCHAR(200), default='', comment="数据库链接地址")
    enabled = Column(Integer, default=1, comment="是否启用：1是，0否")
    remark = Column(VARCHAR(300), default='', comment="备注")

    __table_args__ = ({'comment': '数据库连接信息表'})

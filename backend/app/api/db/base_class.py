import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    # 通用的字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.now, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, server_default=func.now(),
                         server_onupdate=func.now(), comment="更新时间")
    is_delete = Column(Integer, default=0, comment="逻辑删除:0=未删除,1=删除", server_default='0')
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        import re
        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        # 表名格式替换成 下划线_格式 如 MallUser 替换成 mall_user
        return "_".join(name_list).lower()


@as_declarative()
class CommonBase:
    from sqlalchemy import VARCHAR
    # 针对非系统表（fastapi-mysql-generator内置的）通用的字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    create_by = Column(VARCHAR(50), default='', comment="创建者")
    update_by = Column(VARCHAR(50), default='', comment="更新者")
    create_at = Column(DateTime, default=datetime.now, server_default=func.now(), comment="创建时间")
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, server_default=func.now(),
                         server_onupdate=func.now(), comment="更新时间")
    version = Column(Integer, default=1, comment="版本号，用于乐观锁更新", server_default='1')
    valid = Column(Integer, default=1, comment="可用于逻辑删除:0=无效,1=有效", server_default='1')
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        import re
        # 如果没有指定__tablename__  则默认使用model类名转换表名字
        name_list = re.findall(r"[A-Z][a-z\d]*", cls.__name__)
        # 表名格式替换成 下划线_格式 如 MallUser 替换成 mall_user
        return "_".join(name_list).lower()


def gen_uuid() -> str:
    # 生成uuid
    # https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy?rq=1
    return uuid.uuid4().hex

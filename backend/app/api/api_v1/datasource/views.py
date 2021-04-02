#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Lex
# @Desc    :

"""
* 数据库连接信息管理；
* 数据库连接信息下拉列表以中文连接名显示，向后台传送值时使用id；
* 根据选定数据库（连接信息），级联获取数据表清单，表清单以”英文表名+中文表名（即表注释）“相结合的方式显示（如 ent_base_info / 企业基本信息表）；
* 数据展示表格的表头列按上面中文名、下面英文名的方式显示；
* 根据选定数据表，分页查询数据并展示；
"""

from typing import Union, Any, Optional, Generator
from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import sqlalchemy
# from sqlalchemy import text
import datetime, json, re

from api.common import deps
from api.common.logger import logger
from api.utils import response_code

from .schemas import datasource_schema
from .crud.datasource import curd_database_connection_info
from core.config import settings
from api.db.session import engine as _internal_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError


router = APIRouter()

# Constants
SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME = ' / '
SEPARATOR_OF_COLUMNS = ', '


@router.post("/add/database-connection-info", summary="添加数据库连接信息")
async def add_database_connection_info(
        entity: datasource_schema.DatabaseConnectionInfoCreate,
        db: Session = Depends(deps.get_db),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    logger.info(f"添加数据库连接信息->用户id:{token_data.sub}，数据库连接信息名:{entity.connection_name}")
    curd_database_connection_info.create(db=db, obj_in=entity)
    return response_code.resp_200(message="数据库连接信息添加成功")


@router.get("/query/database-connection-info/list", summary="查询数据库连接信息列表")
async def query_database_connection_info_list(
        db: Session = Depends(deps.get_db),
        page: int = Query(1, ge=1, title="页号"),
        page_size: int = Query(10, le=100, title="每页数据量"),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token)
):
    # logger.info(f"查询数据库连接信息列表->用户id:{token_data.sub}当前页{page}长度{page_size}")
    response_result = curd_database_connection_info.query_all(db, page=page, page_size=page_size)
    return response_code.resp_200(data=response_result)


@router.get("/query/database-connection-info", summary="查询数据库连接信息")
async def query_database_connection_info(
        db: Session = Depends(deps.get_db),
        id: int = Query(..., title="查询当前数据库连接信息"),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token)
):
    # logger.info(f"查询数据库连接信息->用户id:{token_data.sub}数据库连接信息:{id}")
    response_result = curd_database_connection_info.query_obj(db, cate_id=id)
    return response_code.resp_200(data=response_result)


@router.post("/modify/database-connection-info", summary="修改数据库连接信息")
async def modify_database_connection_info(
        cate_info: datasource_schema.DatabaseConnectionInfoUpdate,
        db: Session = Depends(deps.get_db),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    logger.info(f"修改数据库连接信息->用户id:{token_data.sub}，数据库连接信息id:{cate_info.id}")
    curd_database_connection_info.update_cate(db=db, obj_in=cate_info)

    return response_code.resp_200(message="修改成功")


@router.post("/del/database-connection-info", summary="删除数据库连接信息")
async def delete_database_connection_info(
        cate_ids: datasource_schema.DatabaseConnectionInfoDel,
        db: Session = Depends(deps.get_db),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    logger.info(f"删除数据库连接信息->用户id:{token_data.sub}，数据库连接信息id:{cate_ids.ids}")
    for cate_id in cate_ids.ids:
        # curd_database_connection_info.remove(db, id=cate_id)
        curd_database_connection_info.delete(db, id=cate_id)
    return response_code.resp_200(message="删除成功")


@router.post("/enabled/database-connection-info", summary="数据库连接信息开启或关闭")
async def enabled_database_connection_info(
        cate_info: datasource_schema.CategoryEnable,
        db: Session = Depends(deps.get_db),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    logger.info(f"启用数据库连接信息操作->用户id:{token_data.sub}，数据库连接信息id:{cate_info.ids}操作:{cate_info.enabled}")
    for cate_id in cate_info.ids:
        curd_database_connection_info.update_enabled(db, id=cate_id, enabled=cate_info.enabled)
    return response_code.resp_200(message="操作成功")


@router.post("/search/database-connection-info", summary="搜索数据库连接信息")
async def search_database_connection_info(
        cate_info: datasource_schema.DatabaseConnectionInfoSearch,
        db: Session = Depends(deps.get_db),
        token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    logger.info(f"搜索数据库连接信息操作->用户id:{token_data.sub}，搜索{cate_info.keyword}:{cate_info.keyword}"
                f"页码:{cate_info.page}长度{cate_info.page_size}")
    response_result = curd_database_connection_info.search_field(db, cate_info=cate_info)
    return response_code.resp_200(data=response_result)


# ----------- TODO 库表展示开发（农业农村信息库）
def get_db(sqlalchemy_database_url: str) -> Generator:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    try:
        engine = create_engine(sqlalchemy_database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/query/mysql-table-list-legacy", summary="查询选定库表清单(Deprecated)")
async def query_mysql_table_list_legacy(
    db_name: str = settings.MYSQL_DATABASE,
    db_connection_url: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    # token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    """
    直连指定的MySQL实例，根据库名列出其表清单
    """
    logger.info(f'搜索表操作->数据库连接URL:{db_connection_url}, 数据库名:{db_name}')

    # -------------
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    if db_connection_url is not None:
        engine = create_engine(db_connection_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            response_result = await get_mysql_table_list(db_name, db)
            return response_code.resp_200(data=response_result)
        finally:
            db.close()
    else:
        try:
            response_result = await get_mysql_table_list(db_name, db)
            return response_code.resp_200(data=response_result)
        finally:
            pass

    # -------------


async def get_mysql_table_list(db_name, db):
    # 从information_schema.tables查询指定库的表
    # Wrapper raw sql
    table_list_query_statement = text("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = :db_name AND table_name NOT IN ('admin_user', 'admin_role')
            """)
    params_dict = {'db_name': db_name}
    table_list = db.execute(table_list_query_statement, params_dict)
    tables = []
    for table in table_list:
        tables.append(table[0])
    response_result = tables
    logger.info(f'Tables: {tables}')
    return response_result


@router.get("/query/mysql-table-list", summary="查询选定库表清单(Deprecated)")
async def query_mysql_table_list(
    db_name: str = settings.MYSQL_DATABASE,
    table_name: Optional[str] = '',
    db_connection_url: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    # token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    """
    直连指定的MySQL实例，根据库名列出其表清单
    """
    logger.info(f'搜索表操作->数据库连接URL:{db_connection_url}, 数据库名:{db_name}')

    # -------------
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    _engine = _internal_engine

    if db_connection_url is not None:
        engine = create_engine(db_connection_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        try:
            # TODO -----------------------
            _engine = engine
            # 获取数据库名列表
            insp = sqlalchemy.inspect(_engine)
            logger.info(f'insp.get_schema_names() -> {insp.get_schema_names()}')

            # 获取表名列表
            _engine.table_names()
            logger.info(f'_engine.table_names() -> {_engine.table_names()}')

            # 获取表字段列表
            md = sqlalchemy.MetaData()
            table = sqlalchemy.Table(table_name, md, autoload=True, autoload_with=_engine)
            columns = table.c
            logger.info(f'columns: {columns}')
            # TODO -----------------------
            response_result = await get_mysql_table_list(db_name, db)
            return response_code.resp_200(data=response_result)
        finally:
            db.close()
    else:
        # TODO -----------------------
        # 获取数据库名列表
        insp = sqlalchemy.inspect(_engine)
        logger.info(f'insp.get_schema_names() -> {insp.get_schema_names()}')

        # 获取表名列表
        _engine.table_names()
        logger.info(f'_engine.table_names() -> {_engine.table_names()}')

        # 获取表字段列表
        md = sqlalchemy.MetaData()
        table = sqlalchemy.Table('mall_goods', md, autoload=True, autoload_with=_engine)
        columns = table.c
        logger.info(f'columns: {columns}')
        # TODO -----------------------
        try:
            response_result = await get_mysql_table_list(db_name, db)
            return response_code.resp_200(data=response_result)
        finally:
            pass

    # -------------


@router.get("/query/table-list", summary="查询选定库表清单")
async def query_table_list(
    db_connection_id: int = 1,
    db: Session = Depends(deps.get_db),
    token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    """
    直连指定的数据库连接信息对应的实例，根据库名列出其表清单，若未选定，则提示；
    """
    logger.info(f'搜索表清单操作->数据库连接id: {db_connection_id}')

    # -------------
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    if db_connection_id is None or db_connection_id <= 0:
        logger.info('未指定数据库连接')
        return response_code.resp_with_custom_message(message='未指定数据库连接')

    # 根据指定的数据库连接名查询数据库连接信息
    db_connection_info_dict = curd_database_connection_info.query_obj(db, cate_id=db_connection_id)
    if len(db_connection_info_dict) == 0:
        logger.info('未找到指定的数据库连接')
        return response_code.resp_with_custom_message(message='未找到指定的数据库连接')

    connection_url = db_connection_info_dict['connection_url']
    db_type_ = db_connection_info_dict['database_type']
    db_type_lower = db_type_.lower()
    _warn_msg = f'暂不支持 [{db_type_}] 数据库类型'
    if db_type_lower == 'MySQL'.lower():
        # TODO Construct database connection url.
        _url = f"mysql+mysqlconnector://{db_connection_info_dict['username']}:{db_connection_info_dict['password']}@" \
               f"{db_connection_info_dict['host']}/{db_connection_info_dict['database_name']}" \
               f"?charset={db_connection_info_dict['charset']}"
        _connection_url = connection_url if connection_url.find('://') != -1 else _url
    elif db_type_lower == 'Oracle'.lower():
        # TODO Not implement yet!
        logger.info(_warn_msg)
        return response_code.resp_with_custom_message(message=_warn_msg)
    elif db_type_lower == 'PostgreSQL'.lower():
        # TODO Not implement yet!
        logger.info(_warn_msg)
        return response_code.resp_with_custom_message(message=_warn_msg)
    elif db_type_lower == 'SQL Server'.lower():
        # TODO Not implement yet!
        logger.info(_warn_msg)
        return response_code.resp_with_custom_message(message=_warn_msg)
    elif db_type_lower == 'SQLite'.lower():
        # TODO Not implement yet!
        logger.info(_warn_msg)
        return response_code.resp_with_custom_message(message=_warn_msg)
    else:
        _warn_msg = f'不支持的数据库类型：{db_type_lower}，当前仅支持数据库类型：MySQL/MariaDB/Oracle/PostgreSQL/SQL Server/SQLite'
        logger.info(_warn_msg)
        return response_code.resp_with_custom_message(message=_warn_msg)

    try:
        engine = create_engine(_connection_url, pool_pre_ping=True, echo=settings.DEBUG)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # 获取数据库名列表
        insp = sqlalchemy.inspect(engine)
        logger.debug(f'insp.get_schema_names() -> {insp.get_schema_names()}')

        # 获取表清单
        table_names = engine.table_names()
        logger.debug(f'engine.table_names() -> {table_names}')
        logger.debug(f'engine.table_names() -> {engine.table_names()}')

        # 获取表字段列表
        md = sqlalchemy.MetaData()
        # table = sqlalchemy.Table(table_name, md, autoload=True, autoload_with=engine)
        # columns = table.c
        # logger.info(f'columns: {columns}')

        # TODO 从表的注释得到表中文名 #get_table_en_and_cn_names
        # table_en_and_cn_names = {k:v  for t in table_names}
        tables_with_comments = {}
        for _table_name in table_names:
            _table = sqlalchemy.Table(_table_name, md, autoload=True, autoload_with=engine)
            _comment = _table.comment
            logger.info(f'_table->{_table_name}, _comment->{_comment}')
            tables_with_comments[_table_name] = _comment
        logger.info(f'default_db_name->{insp.default_schema_name}, tables_with_comments->{tables_with_comments}')
        table_en_and_cn_names = tables_with_comments
        table_names_with_cn_names = [SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME.join([d, table_en_and_cn_names[d]])
                                     if table_en_and_cn_names[d] and len(table_en_and_cn_names[d].strip()) > 0 else d
                                     for d in table_en_and_cn_names]

        # response_result = table_names
        response_result = table_names_with_cn_names
        return response_code.resp_200(data=response_result)
    except ArgumentError as ae:
        logger.error(f'Exception parsing db_connection_url: {ae}')
        return response_code.resp_with_custom_message(message='解析数据库链接URL失败')
    except ProgrammingError as pe:
        from api.common.database_error_wrapper import GoodMessageDatabaseException
        _error_msg = GoodMessageDatabaseException.get_friendly_error_message(pe)
        logger.error(_error_msg)
        return response_code.resp_with_custom_message(message=_error_msg)
    except Exception as e:  # TODO
        _error_msg = f'Exception getting table list by database connection url: {_connection_url}, error: {e}'
        logger.error(_error_msg)
        # return response_code.resp_with_custom_message(message=_error_msg)
        return response_code.resp_with_custom_message(message=e.orig.msg)
    finally:
        db.close()


@router.get("/query/mysql-table-data-legacy", summary="查询选定表数据(Deprecated)")
async def query_mysql_table_data_legacy(
    db_name: str = settings.MYSQL_DATABASE,
    table_name: Optional[str] = '',
    db_connection_url: Optional[str] = None,
    page: int = Query(1, ge=1, title="当前页号"),
    page_size: int = Query(10, le=100, title="每页数据量"),
    db: Session = Depends(deps.get_db),
    # token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    """
    直连指定的MySQL实例，根据库名和表列出其数据
    """
    logger.info(f'查询表数据->数据库连接URL: {db_connection_url}, 库名: {db_name}, 表名: {table_name}, 页号: {page}, 每页数据量: {page_size}')
    if db_connection_url:
        logger.warn(f'Not implement yet...')

    # -------------
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    _engine = _internal_engine

    # ------------- 、、、、、、、、、、、、、、
    if db_connection_url is not None:
        engine = create_engine(db_connection_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            response_result = await get_mysql_table_list(db_name, db)
            return response_code.resp_200(data=response_result)
        finally:
            db.close()
    else:
        try:
            response_result = await get_mysql_table_list(db_name, db)
            return response_code.resp_200(data=response_result)
        finally:
            pass
    # -------------、、、、、、、、、、、、、、、、、、


@router.get("/query/mysql-table-data", summary="查询选定表数据(Deprecated)")
async def query_mysql_table_data(
    db_name: str = settings.MYSQL_DATABASE,
    table_name: Optional[str] = 'mall_category',
    db_connection_url: Optional[str] = None,
    page_no: int = Query(1, ge=1, title="当前页号"),
    page_size: int = Query(10, le=100, title="每页数据量"),
    db: Session = Depends(deps.get_db),
    # token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    """
    TODO 直连指定的MySQL实例，根据库名和表列出其数据
    """
    logger.info(f'查询表数据->数据库连接URL: {db_connection_url}, 库名: {db_name}, 表名: {table_name}, 页号: {page_no}, 每页数据量: {page_size}')
    if db_connection_url is not None and db_connection_url.strip() == '':
        logger.debug(f'Not implement yet...')
        db_connection_url = None

    if table_name is None or table_name.strip() == '':
        return response_code.resp_200(data='数据表未指定')

    # -------------
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = _internal_engine

    if db_connection_url is not None:

        try:
            # TODO -----------------------
            engine = create_engine(db_connection_url, pool_pre_ping=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            db = SessionLocal()

            # TODO 根据指定的数据库链接及库名表名查数据
        except ArgumentError as ae:
            logger.error(f'Exception parsing db_connection_url: {ae}')
            return response_code.resp_with_custom_message(message='解析数据库链接URL失败')
        finally:
            db.close()
    else:
        # TODO -----------------------

        # 获取数据库名列表
        insp = sqlalchemy.inspect(engine)
        databases = insp.get_schema_names()

        # 获取表名列表
        tables = insp.get_table_names()

        # 获取表字段列表
        md = sqlalchemy.MetaData()
        _table = sqlalchemy.Table(table_name, md, autoload=True, autoload_with=engine)
        columns = [c.name for c in _table.c]
        # 获取字段英文名、字段中文名及类型
        columns_with_comments_and_types = [(c.name, c.comment, c.type) for c in _table.c]

        query_columns = SEPARATOR_OF_COLUMNS.join(columns)

        column_names_with_comment = [SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME.join([c.name, c.comment if c.comment else 'NA']) for c in _table.c]
        columns_for_frontend = [c.comment if c.comment and c.comment.strip() and len(c.comment) > 0 else c.name for
                                c in _table.c]
        # 利用正则表达式对注释进行处理，只取前面有效部分，从而得到列中文名
        pattern = r'[\s\t|:|：|-]'
        columns_for_frontend_clean = [
            re.split(pattern, c.comment.strip())[0] if c.comment and c.comment.strip() and len(
                c.comment) > 0 else c.name for c in _table.c]

        columns_for_frontend_clean_complex = []
        for c in _table.c:
            if c.name.lower() == 'id':
                # id 列不需要整合中英文，只需英文列名即可！
                columns_for_frontend_clean_complex.append(c.name.upper())
                continue
            elif c.comment and c.comment.strip() and len(c.comment) > 0:
                column_frontend_part_zh_cn = re.split(pattern, c.comment.strip())[0]
            else:
                # column_frontend_part_zh_cn = 'NA'
                column_frontend_part_zh_cn = ''  # 用空白字符串，避免前台展示难看
            column_frontend = SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME.join([c.name, column_frontend_part_zh_cn])
            columns_for_frontend_clean_complex.append(column_frontend)

        print(f'column_names_with_comment -> {column_names_with_comment}')
        print(f'columns_for_frontend -> {columns_for_frontend}')
        print(f'columns_for_frontend_clean -> {columns_for_frontend_clean}')
        print(f'columns_for_frontend_clean_complex -> {columns_for_frontend_clean_complex}')

        raw_sql = f'SELECT {query_columns} FROM {table_name} LIMIT {(page_no - 1) * page_size}, {page_size}'
        raw_statement = text(raw_sql)

        raw_sql_for_total = f'SELECT count(*) FROM {table_name}'
        raw_statement_for_total = text(raw_sql_for_total)

        data_items = []
        total = 0

        with engine.connect() as connection:
            data_list = connection.execute(raw_statement)
            current_size = data_list.rowcount
            # Get total of the _table.
            total = connection.execute(raw_statement_for_total).first()[0]
            print(f'total-> {total}')

            for data in data_list:
                # print(f'data -> {data}')
                # print('--------------------------------------')
                data_item = {c: str(d) if isinstance(d, datetime.datetime) else d for c, d in
                             zip(columns_for_frontend_clean_complex, data)}
                # print(f'data_item -> {data_item}')
                # print('--------------------------------------')
                data_items.append(data_item)

        # print('--------------------------------------')
        # result = {"code": 200, "message": "success"}
        # result.update({"data": {"items": data_items}, "total": total})
        # response_json = json.dumps(result)
        # print(f'response_json -> {response_json}')

        # TODO -----------------------
        response_result = {"data": {"items": data_items}, "total": total}
        return response_code.resp_200(data=response_result)

    # -------------


@router.get("/query/table-data", summary="查询选定表数据")
async def query_table_data(
    db_connection_id: int = 1,
    table_name: Optional[str] = None,
    page_no: int = Query(1, ge=1, title="当前页号"),
    page_size: int = Query(10, le=100, title="每页数据量"),
    db: Session = Depends(deps.get_db),
    token_data: Union[str, Any] = Depends(deps.check_jwt_token),
):
    """
    直连指定的MySQL实例，根据数据库连接信息分页查询出选定的表的数据
    """
    logger.info(f'查询表数据->数据库连接id: {db_connection_id}, 表名: {table_name}, 页号: {page_no}, 每页数据量: {page_size}')

    if db_connection_id is None or db_connection_id <= 0:
        logger.info('未指定数据库连接')
        return response_code.resp_with_custom_message(message='未指定数据库连接')

    if table_name is None or table_name.strip() == '':
        logger.info('未指定数据表')
        return response_code.resp_with_custom_message(data='未指定数据表')
    # 处理前端传过来的表名，只留英文名
    table_en_name = table_name if table_name.find(SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME) == -1 else table_name.split(SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME)[0]
    logger.info(f'table_en_name -> {table_en_name}')

    # 根据指定的数据库连接名查询数据库连接信息
    db_connection_info_dict = curd_database_connection_info.query_obj(db, cate_id=db_connection_id)
    if len(db_connection_info_dict) == 0:
        logger.info('未找到指定的数据库连接')
        return response_code.resp_with_custom_message(message='未找到指定的数据库连接')

    db_type_ = db_connection_info_dict['database_type']
    db_type_lower = db_type_.lower()
    _warn_msg = f'尚不支持的数据库类型 [{db_type_}]'
    try:
        if db_type_lower == 'MySQL'.lower():
            response_result = await do_query_table_data_mysql(db, db_connection_info_dict, page_no, page_size, table_en_name)
            return response_code.resp_200(data=response_result)
        elif db_type_lower == 'Oracle'.lower():
            # TODO Not implement yet!
            logger.info(_warn_msg)
            return response_code.resp_with_custom_message(message=_warn_msg)
        elif db_type_lower == 'PostgreSQL'.lower():
            # TODO Not implement yet!
            logger.info(_warn_msg)
            return response_code.resp_with_custom_message(message=_warn_msg)
        elif db_type_lower == 'SQL Server'.lower():
            # TODO Not implement yet!
            logger.info(_warn_msg)
            return response_code.resp_with_custom_message(message=_warn_msg)
        elif db_type_lower == 'SQLite'.lower():
            # TODO Not implement yet!
            logger.info(_warn_msg)
            return response_code.resp_with_custom_message(message=_warn_msg)
        else:
            _warn_msg = f'不支持的数据库类型：{db_type_lower}，当前仅支持数据库类型：MySQL/Oracle/PostgreSQL/SQL Server/SQLite'
            logger.info(_warn_msg)
            return response_code.resp_with_custom_message(message=_warn_msg)
    except ArgumentError as ae:
        logger.error(f'Exception parsing db_connection_url: {ae}')
        return response_code.resp_with_custom_message(message='解析数据库链接URL失败')
    except ProgrammingError as pe:
        from api.common.database_error_wrapper import GoodMessageDatabaseException
        _error_msg = GoodMessageDatabaseException.get_friendly_error_message(pe)
        logger.error(_error_msg)
        return response_code.resp_with_custom_message(message=_error_msg)
    except Exception as e:  # TODO
        _error_msg = f'Exception getting table data, error: {e}'
        logger.error(_error_msg)
        return response_code.resp_with_custom_message(message=_error_msg)


async def do_query_table_data_mysql(db, db_connection_info_dict, page_no, page_size, table_en_name):
    # TODO Construct database connection url.
    _url = f"mysql+mysqlconnector://{db_connection_info_dict['username']}:{db_connection_info_dict['password']}@" \
           f"{db_connection_info_dict['host']}/{db_connection_info_dict['database_name']}" \
           f"?charset={db_connection_info_dict['charset']}"
    connection_url = db_connection_info_dict['connection_url']
    _connection_url = connection_url if connection_url.find('://') != -1 else _url
    try:

        # ----------------------------------------------------- begin
        db, engine = await construct_db_engine(_connection_url)

        # 获取表字段列表
        md = sqlalchemy.MetaData()
        _table = sqlalchemy.Table(table_en_name, md, autoload=True, autoload_with=engine)
        columns = [c.name for c in _table.c]
        # 获取字段英文名、字段中文名及类型
        columns_with_comments_and_types = [(c.name, c.comment, c.type) for c in _table.c]
        query_columns = SEPARATOR_OF_COLUMNS.join(columns)

        # 对于 MySQL，由于建表不规范可能会在表名中包含中文、甚至“-”等特殊符号，故添加上点号（``）来修饰，避免导致执行SQL语句报异常！
        table_en_name_fixed = f'`{table_en_name}`'
        raw_sql = f'SELECT {query_columns} FROM {table_en_name_fixed} LIMIT {(page_no - 1) * page_size}, {page_size}'
        raw_statement = text(raw_sql)
        raw_sql_for_total = f'SELECT count(*) FROM {table_en_name_fixed}'
        raw_statement_for_total = text(raw_sql_for_total)

        # ----------------------------------------------------- end

        data_items = []

        with engine.connect() as connection:
            data_list = connection.execute(raw_statement)
            current_size = data_list.rowcount
            # Get total of the _table.
            total = connection.execute(raw_statement_for_total).first()[0]
            print(f'total-> {total}')

            columns_for_frontend_clean_complex = await construct_frontend_columns(_table)

            for data in data_list:
                data_item = {c: str(d) if isinstance(d, datetime.datetime) else d for c, d in
                             zip(columns_for_frontend_clean_complex, data)}
                data_items.append(data_item)

        response_result = {"data": {"items": data_items}, "total": total}
        logger.debug(f'response_result->{response_result}')
        return response_result
        # return response_code.resp_200(data=response_result)
    # except ArgumentError as ae:
    #     logger.error(f'Exception parsing db_connection_url: {ae}')
    #     return response_code.resp_with_custom_message(message='解析数据库链接URL失败')
    # except Exception as e:  # TODO
    #     _error_msg = f'Exception getting table list by database connection url: {_connection_url}, error: {e}'
    #     logger.error(_error_msg)
    #     return response_code.resp_with_custom_message(message=_error_msg)
    finally:
        db.close()


async def construct_db_engine(_connection_url):
    engine = create_engine(_connection_url, pool_pre_ping=True, echo=settings.DEBUG)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db, engine


async def construct_frontend_columns(_table):
    # 利用正则表达式对注释进行处理，只取前面有效部分，从而得到列中文名
    pattern = r'[\s\t|:|：|-|——|,|，|;|；]'
    columns_for_frontend_clean = [
        re.split(pattern, c.comment.strip())[0] if c.comment and c.comment.strip() and len(
            c.comment) > 0 else c.name for c in _table.c]
    print(f'columns_for_frontend_clean -> {columns_for_frontend_clean}')
    columns_for_frontend_clean_complex = []
    for c in _table.c:
        if c.name.lower() == 'id':
            # id 列不需要整合中英文，只需英文列名即可！
            columns_for_frontend_clean_complex.append(c.name.upper())
            continue
        elif c.comment and c.comment.strip() and len(c.comment) > 0:
            column_frontend_part_zh_cn = re.split(pattern, c.comment.strip())[0]
        else:
            # column_frontend_part_zh_cn = 'NA'
            column_frontend_part_zh_cn = ''  # 用空白字符串，避免前台展示难看
        column_frontend = SEPARATOR_BETWEEN_EN_NAME_AND_CN_NAME.join([c.name, column_frontend_part_zh_cn])
        columns_for_frontend_clean_complex.append(column_frontend)
    print(f'columns_for_frontend_clean_complex -> {columns_for_frontend_clean_complex}')
    return columns_for_frontend_clean_complex

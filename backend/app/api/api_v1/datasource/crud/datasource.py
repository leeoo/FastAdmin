#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author  : Lex
# @Desc    :
"""

"""

from pydantic import conint
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from api.common.curd_base import CRUDBase
from api.models.datasource import DatabaseConnectionInfo
from ..schemas import datasource_schema


class CRUDDatasource(CRUDBase[
                         DatabaseConnectionInfo, datasource_schema.DatabaseConnectionInfoCreate, datasource_schema.DatabaseConnectionInfoUpdate]):

    def query_obj(self, db: Session, *, cate_id: int) -> dict:
        """
        查询单条数据
        :param db:
        :param cate_id:
        :return:
        """
        # obj = self.get(db=db, id=cate_id)
        obj = self.get_new(db=db, id=cate_id)
        if not obj:
            return {}
        return {"id": obj.id,
                "connection_name": obj.connection_name,
                "database_type": obj.database_type,
                "database_version": obj.database_version,
                "host": obj.host,
                "port": obj.port,
                "database_name": obj.database_name,
                "charset": obj.charset,
                "username": obj.username,
                "password": obj.password,
                "connection_url": obj.connection_url,
                "enabled": obj.enabled,
                "remark": obj.remark,
                'create_at': obj.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                'update_at': obj.update_at.strftime('%Y-%m-%d %H:%M:%S'),
                'create_by': obj.create_by,
                'update_by': obj.update_by,
                # 'version': obj.version,
                'valid': obj.valid
                }

    @staticmethod
    def search_field(db: Session, *, cate_info: datasource_schema.DatabaseConnectionInfoSearch):
        temp_page = (cate_info.page - 1) * cate_info.page_size
        # 查询数量包含关键词的数量
        total = db.query(func.count(DatabaseConnectionInfo.id)).filter(DatabaseConnectionInfo.valid == 1,
            or_(DatabaseConnectionInfo.connection_name.contains(cate_info.keyword),
                DatabaseConnectionInfo.database_name.contains(cate_info.keyword),
                DatabaseConnectionInfo.database_type.contains(cate_info.keyword)
                )).scalar()
        # 查询name和front_desc包含搜索关键词的数据并分页
        search_obj = db.query(DatabaseConnectionInfo).filter(DatabaseConnectionInfo.valid == 1,
            or_(DatabaseConnectionInfo.connection_name.contains(cate_info.keyword),
                DatabaseConnectionInfo.database_name.contains(cate_info.keyword),
                DatabaseConnectionInfo.database_type.contains(cate_info.keyword)
                )).offset(
            temp_page).limit(cate_info.page_size).all()

        items = [{
            "id": obj.id,
            "connection_name": obj.connection_name,
            "database_type": obj.database_type,
            "database_version": obj.database_version,
            "host": obj.host,
            "port": obj.port,
            "database_name": obj.database_name,
            "charset": obj.charset,
            "username": obj.username,
            "password": obj.password,
            "connection_url": obj.connection_url,
            "enabled": obj.enabled,
            "remark": obj.remark,
            'create_at': obj.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            'update_at': obj.update_at.strftime('%Y-%m-%d %H:%M:%S'),
            'create_by': obj.create_by,
            'update_by': obj.update_by,
            # 'version': obj.version,
            'valid': obj.valid
          } for obj in search_obj]
        return {
            "items": items,
            "total": total
        }

    @staticmethod
    def query_all(db: Session, *, page: int = 1, page_size: conint(le=100) = 10) -> dict:
        """
        查询数据源列表，过滤掉已删除和已停用的；
        :param db:
        :param page:
        :param page_size:
        :return:
        """
        temp_page = (page - 1) * page_size
        # 查询数量
        total = db.query(func.count(DatabaseConnectionInfo.id)).filter(DatabaseConnectionInfo.valid == 1,
                                                                       DatabaseConnectionInfo.enabled == 1
                                                                       ).scalar()
        # 查询结果集
        query_obj = db.query(DatabaseConnectionInfo).filter(DatabaseConnectionInfo.valid == 1,
                                                            DatabaseConnectionInfo.enabled == 1
                                                            ).offset(
            temp_page).limit(page_size).all()

        items = [{"id": obj.id,
                  "connection_name": obj.connection_name,
                  "database_type": obj.database_type,
                  "database_version": obj.database_version,
                  "host": obj.host,
                  "port": obj.port,
                  "database_name": obj.database_name,
                  "charset": obj.charset,
                  "username": obj.username,
                  "password": obj.password,
                  "connection_url": obj.connection_url,
                  "enabled": obj.enabled,
                  "remark": obj.remark,
                  "create_by": obj.create_by,
                  "update_by": obj.update_by,
                  'create_at': obj.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                  'update_at': obj.update_at.strftime('%Y-%m-%d %H:%M:%S')
                  } for obj in query_obj]
        return {
            "items": items,
            "total": total
        }

    def create(self, db: Session, *, obj_in: datasource_schema.DatabaseConnectionInfoCreate) -> DatabaseConnectionInfo:
        db_obj = DatabaseConnectionInfo(
            connection_name=obj_in.connection_name,
            database_type=obj_in.database_type,
            database_version=obj_in.database_version,
            host=obj_in.host,
            port=obj_in.port,
            database_name=obj_in.database_name,
            charset=obj_in.charset,
            username=obj_in.username,
            password=obj_in.password,
            connection_url=obj_in.connection_url,
            enabled=obj_in.enabled,
            remark=obj_in.remark,
            create_by=obj_in.create_by,
            update_by=obj_in.update_by
            # ,
            # create_at=obj_in.create_at,
            # update_at=obj_in.update_at
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_cate(db: Session, *, obj_in: datasource_schema.DatabaseConnectionInfoUpdate):
        db.query(DatabaseConnectionInfo).filter(DatabaseConnectionInfo.id == obj_in.id).update({
            DatabaseConnectionInfo.connection_name: obj_in.connection_name,
            DatabaseConnectionInfo.database_type: obj_in.database_type,
            DatabaseConnectionInfo.database_version: obj_in.database_version,
            DatabaseConnectionInfo.host: obj_in.host,
            DatabaseConnectionInfo.port: obj_in.port,
            DatabaseConnectionInfo.database_name: obj_in.database_name,
            DatabaseConnectionInfo.charset: obj_in.charset,
            DatabaseConnectionInfo.username: obj_in.username,
            DatabaseConnectionInfo.password: obj_in.password,
            DatabaseConnectionInfo.connection_url: obj_in.connection_url,
            DatabaseConnectionInfo.enabled: obj_in.enabled,
            DatabaseConnectionInfo.remark: obj_in.remark,
            DatabaseConnectionInfo.update_by: obj_in.update_by,
            DatabaseConnectionInfo.update_at: obj_in.update_at,
            DatabaseConnectionInfo.version: obj_in.version + 1
        })
        db.commit()

    @staticmethod
    def update_enabled(db: Session, *, id: int, enabled: int):
        db.query(DatabaseConnectionInfo).filter(DatabaseConnectionInfo.id == id).update(
            {DatabaseConnectionInfo.enabled: enabled})  # TODO 需要更新版本及更新时间！
        db.commit()


curd_database_connection_info = CRUDDatasource(DatabaseConnectionInfo)

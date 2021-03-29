import request from '@/utils/request'

export function getList(params) {
  return request(
    '/auth/table/list',
    'get',
    params
  )
}

// 下拉框数据库连接信息数据
export function getDatasourceConnectionInfoSelectList(params) {
  return request(
    '/datasource/query/database-connection-info/list',
    'get',
    params
  )
}

// 下拉框表清单数据
export function getTableSelectList(params) {
  return request(
    '/datasource/query/table-list',
    'get',
    params
  )
}

// 表数据
export function getTableDataList(params) {
  return request(
    '/datasource/query/table-data',
    'get',
    params
  )
}


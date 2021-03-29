import request from '@/utils/request'
// 列表
export function getList(params) {
  return request(
    '/datasource/search/database-connection-info',
    'post',
    params
  )
}
// 新增
export function add(params) {
  return request(
    '/datasource/add/database-connection-info',
    'post',
    params
  )
}
// 修改
export function edit(params) {
  return request(
    '/datasource/modify/database-connection-info',
    'post',
    params
  )
}
// 删除
export function del(params) {
  return request(
    '/datasource/del/database-connection-info',
    'post',
    params
  )
}
// 状态
export function editStatus(params) {
  return request(
    '/datasource/enabled/database-connection-info',
    'post',
    params
  )
}

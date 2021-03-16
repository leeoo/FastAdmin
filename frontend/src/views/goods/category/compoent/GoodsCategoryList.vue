<template>
  <div class="app">
    <el-table v-loading="loading" :data="dataList">
      <el-table-column label="ID" align="center" prop="id" />
      <el-table-column label="名称" align="center" prop="name" />
      <el-table-column label="链接" align="center" prop="icon_url" />
      <el-table-column label="描述" align="center" prop="front_desc" />
      <el-table-column label="是否启用" align="center" prop="enabled" />
      <el-table-column label="创建时间" align="center" prop="create_time" />
      <el-table-column label="排序" align="center" prop="sort_order" />
    </el-table>

    <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="queryParams.page"
      :limit.sync="queryParams.page_size"
      @pagination="getList"
    />

  </div>
</template>

<script>

  import { listView } from '@/api/goods'

  export default {
    name: 'GoodsCategoryList',
    data() {
      return {
        // 遮罩层
        loading: true,
        // 分页总数
        total: null,
        // 数据列表
        dataList: [],
        // 查询参数
        queryParams: {
          page: 1,
          page_size: 10
        }
      }
    },
    created() {
      this.getList()
    },
    methods: {
      /** 查询门户资讯列表 */
      getList() {
        this.loading = true
        listView(this.queryParams).then(res => {
          this.dataList = res.data.items
          this.total = res.data.total
          this.loading = false
        })
      }
    }
  }
</script>

<style scoped>

</style>

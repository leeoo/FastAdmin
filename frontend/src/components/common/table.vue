<template>
    <div class="common-table-component">
        <el-table class="common-table" v-loading="loading" :data="dataList" stripe>
          <el-table-column
            v-for="(item, index) in columns"
            show-overflow-tooltip
            :key="index"
            :label="item.label"
            align="center"
            :prop="item.prop"
            :minWidth="item.minWidth"
            :formatter="item.formatter">
          </el-table-column>
          <el-table-column
            label="操作"
            align="center"
            :width="100"
            fixed="right">
            <template slot-scope="scope">
              <div class="common-table-btn">
                <el-button type="text" title="编辑" icon="el-icon-edit" @click="onEdit(scope.row)"></el-button>
               <!--
                <el-button class="mr10" type="text" icon="el-icon-edit" @click="onEdit(scope.row)"></el-button>
               -->
                <el-button slot="reference" type="text" :title="scope.row.enabled == 0 ? '启用' : '停用'" :icon="scope.row.enabled == 0 ? 'el-icon-check' : 'el-icon-close'" @click="onEditStatus(scope.row.id, scope.row.enabled)"></el-button>
                <el-button type="text" title="删除" icon="el-icon-delete" slot="reference" @click="onDel(scope.row.id)"></el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          v-show="total > 0"
          :total="total"
          :page-size.sync="form.page_size"
          :current-page.sync="form.page"
          @size-change="onChangePageSize"
          @current-change="onChangePage"
          layout="total, sizes, prev, pager, next, jumper"
        />
    </div>
</template>
script>
  import { getList, add, edit, del, editStatus } from '@/api/datasource'
  export default {
    name: 'myTable',
    data() {
      return {
        loading: false,
        total: 0, // 分页总数
        dataList: [], // 数据列表
        columns:[],
        searchForm: {
          page: 1,
          page_size: 10
        }
      }
    },
    mounted(){
    },
    methods:{
      // 切换页面大小
      onChangePageSize(page_size){
        this.searchForm.page_size = page
        this.getList()
      },
      // 切换页面
      onChangePage(page){
        this.searchForm.page = page
      },
      // 设置表数据
      setData(data,total){
        this.dataList = data
        this.total = total
      }
    }
  }
</script>

<style scoped lang="scss">
.common-form-item{
  width: 50%;
  display: inline-block;
  .el-select {
    width: 100%;
  }
}
</style>

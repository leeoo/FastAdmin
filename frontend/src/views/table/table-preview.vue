<template>
  <div class="common-page">
  <el-form :inline="true" :model="form" class="demo-form-inline">
    <el-form-item  label="数据库信息">
      <el-select filterable style="width: 350px" v-model="form.db_connection_id" placeholder="请选择数据库" @change="onChangeConn">
        <el-option
          v-for="(item, index) in datasourceConnectionSelectList"
          :key="index"
          :label="item.connection_name"
          :value="item.id"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="数据库表">
      <el-select filterable style="width: 400px" v-model="form.table_name" placeholder="请选择数据库表" @change="getDataList()">
        <el-option
          v-for="(item, index) in selectList"
          :key="index"
          :label="item"
          :value="item"></el-option>
      </el-select>
    </el-form-item>
    <!--
    <el-form-item>
      <el-button type="primary" @click="getDataList">查询</el-button>
    </el-form-item>
    -->
  </el-form>
  <el-table class="common-table" v-loading="loading" :data="dataList" stripe v-if="form.table_name">
    <el-table-column
      v-for="(item, index) in columns"
      show-overflow-tooltip
      :key="index"
      :label="item.label"
      align="center"
      :prop="item.prop"
      :formatter="item.formatter"
      :minWidth="getWidth(item.label, item.prop)">
      <template slot="header">
        <div>{{item.prop}}</div>
        <div>{{item.label}}</div>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination
    v-show="total>0"
    :total="total"
    :page-size.sync="form.page_size"
    :current-page.sync="form.page_no"
    @size-change="onChangePageSize"
    @current-change="onChangePage"
    layout="total, sizes, prev, pager, next, jumper"
  />
  </div>
</template>

<script>
  const SPECIFIED = ['valid', 'enabled', 'checked', 'is_delete']
  import { getDatasourceConnectionInfoSelectList, getTableSelectList, getTableDataList } from '@/api/table'
  export default {
    name: 'myTable',
    data() {
      return {
        loading: false,
        // 分页总数
        total: 0,
        // 数据列表
        dataList: [],
        columns:[],
        selectList: [],
        datasourceConnectionSelectList: [],
        form: {
          db_connection_id: 1,
          table_name: '',
          page_no: 1,
          page_size: 10
        }
      }
    },
    mounted(){
      this.getSelectList()
      this.getDatabaseConnectionSelectList()
    },
    methods:{
      // 切换页面大小
      onChangePageSize(page_size){
        this.form.page_size = page_size
        this.getDataList()
      },
      // 切换页面
      onChangePage(page_no){
        this.form.page_no = page_no
        this.getDataList()
      },
      // 动态设置宽度
      getWidth(label, prop){
        let width = 100
        let cnWidth = label.length * 20
        let enWidth = prop.length * 10
        width = cnWidth > enWidth ? cnWidth : enWidth
        if(label.indexOf('时间')>-1 || label.indexOf('日期')>-1 && width < 160){
         width = 160
        }
        return width > 100 ? width :　100
      },
      //改变数据库链接信息
      onChangeConn(value){
        if(value){
          this.selectList = []
          this.dataList = []
          this.columns = []
          this.form.table_name = ''
          this.getSelectList(value)
        }
      },
      //获取数据库连接信息列表下拉框
      getDatabaseConnectionSelectList(){
        getDatasourceConnectionInfoSelectList({page: 1,page_size:　100}).then(res => {
          if (res.code===200){
            this.datasourceConnectionSelectList = res.data.items
          }
        })
      },
      //获取表清单下拉框
      getSelectList(id){
        getTableSelectList({db_connection_id: id}).then(res => {
          if (res.code===200){
            this.selectList = res.data
          }
        })
      },
      // 获取表数据
      getDataList(){
        this.columns = []
        this.dataList = []
        this.loading = true
        getTableDataList(this.form).then(res => {
          if (res.code===200){
            let columns = []
            let data = []
            res.data.data.items.map((item, index) => {
              let obj = {}
              for (let key in item) {
                let arr = key.split(' / ')
                if(index===0){
                  let obj = {
                    prop: arr.length > 0 ? arr[0] : '',
                    label: arr.length > 1 ? arr[1] : '',
                  }
                  if(obj.prop && SPECIFIED.indexOf(obj.prop)>-1){
                    obj['formatter'] = (row, column, cellValue, index) => {
                      return cellValue === 1 ? '√' : '×'
                    }
                  }
                  columns.push(obj)
                }
               obj[arr[0]] = item[key]
              }
              data.push(obj)
            })
            this.total = res.data.total
            this.columns = columns
            this.dataList = data
          }
          this.loading = false
        })
      }
    }
  }
</script>

<style scoped>
.table-page{
  padding: 30px;
}
.my-table{
  margin-bottom:20px;
}
</style>

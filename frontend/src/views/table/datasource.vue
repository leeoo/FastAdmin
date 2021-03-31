<template>
  <div class="common-page">
    <el-form :inline="true" :model="searchForm" class="demo-form-inline" @submit.native.prevent>
      <el-form-item label="数据库信息">
        <el-input
         v-model="searchForm.keyword"
         style="width:250px"
         placeholder="请输入关键字查询"
         clearable
         @keyup.enter.native="getList()"
         @clear="getList()" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="getList">查询</el-button>
        <el-button type="primary" @click="onAdd">新增</el-button>
      </el-form-item>
    </el-form>
    <el-table class="common-table" v-loading="loading" :data="dataList" stripe>
      <template v-for="(item, index) in columns">
        <el-table-column
          v-if="item.prop === 'enabled'"
          :key="index"
          :label="item.label"
          align="center"
          :prop="item.prop"
          :minWidth="item.minWidth">
          <template slot-scope="scope">
            <el-switch
              v-model="scope.row.enabled"
              active-color="#409EFF"
              inactive-color="#C0C4CC"
              :active-value="1"
              :inactive-value="0"
              size="small"
              @change="onEditStatus(scope.row.id, scope.row.enabled)">
            {{scope.row.enabled}} </el-switch>
          </template>
        </el-table-column>
        <el-table-column
          v-else
          show-overflow-tooltip
          :key="index"
          :label="item.label"
          align="center"
          :prop="item.prop"
          :minWidth="item.minWidth"
          :formatter="item.formatter">
        </el-table-column>
      </template>
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
            <!-- <el-button slot="reference" type="text" :title="scope.row.enabled == 0 ? '启用' : '停用'" :icon="scope.row.enabled == 0 ? 'el-icon-check' : 'el-icon-close'" @click="onEditStatus(scope.row.id, scope.row.enabled)"></el-button> -->
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
    <el-dialog
      :title="form.id ? '编辑' : '新增' "
      :visible.sync="visibleDialog"
      width="1000px"
      @close="onClose">
      <el-form ref="form" :model="form" label-width="130px" :rules="rules">
        <el-form-item label="连接名称" prop="connection_name" class="common-form-item">
          <el-input v-model="form.connection_name" placeholder="请输入连接名称"></el-input>
        </el-form-item>
        <el-form-item label="数据库类型" prop="database_type" class="common-form-item">
          <el-select v-model="form.database_type" placeholder="请选择数据库类型">
            <el-option label="MySQL" value="MySQL"></el-option>
            <el-option label="MariaDB" value="MariaDB"></el-option>
            <el-option label="Percona" value="Percona"></el-option>
            <el-option label="Oracle" value="Oracle"></el-option>
            <el-option label="PostgreSQL" value="PostgreSQL"></el-option>
            <el-option label="SQL Server" value="SQL Server"></el-option>
            <el-option label="SQLite" value="SQLite"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据库版本" prop="database_version" class="common-form-item">
          <el-input v-model="form.database_version" placeholder="请输入数据库版本"></el-input>
        </el-form-item>
        <el-form-item label="主机名/IP" prop="host" class="common-form-item">
          <el-input v-model="form.host" placeholder="请输入主机名/IP"></el-input>
        </el-form-item>
        <el-form-item label="端口" prop="port" class="common-form-item">
          <el-input v-model="form.port" placeholder="请输入端口"></el-input>
        </el-form-item>
        <el-form-item label="数据库名" prop="database_name" class="common-form-item">
          <el-input v-model="form.database_name" placeholder="请输入数据库名"></el-input>
        </el-form-item>
        <el-form-item label="字符集" prop="charset" class="common-form-item">
          <el-input v-model="form.charset" placeholder="请输入字符集"></el-input>
        </el-form-item>
        <el-form-item label="用户名" prop="username" class="common-form-item">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password" class="common-form-item">
          <el-input v-model="form.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="是否启用" prop="enabled" class="common-form-item">
          <el-radio-group v-model="form.enabled" placeholder="请选择是否启用">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">停用</el-radio>
          </el-radio-group>
        </el-form-item>
       <!--  <el-form-item label="是否有效" prop="valid" class="common-form-item">
          <el-select v-model="form.valid" placeholder="请选择是否有效">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="停用" :value="0"></el-option>
          </el-select>
        </el-form-item> -->
        <el-form-item label="数据库链接地址" prop="connection_url">
          <el-input v-model="form.connection_url" placeholder="请输入端口"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="visibleDialog = false">取 消</el-button>
        <el-button type="primary" @click="onSubmit">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import { getList, add, edit, del, editStatus } from '@/api/datasource'
  export default {
    name: 'Datasource',
    data() {
      return {
        test: true,
        visibleDialog: false,
        loading: false,
        total: 0, // 分页总数
        dataList: [], // 数据列表
        form: {
          connection_name: '',
          database_type: '',
          database_version: '',
          host: '',
          port: '',
          database_name: '',
          charset: '',
          username: '',
          password: '',
          connection_url: '',
          enabled: 1,
          remark: ''
        },
        rules: {
          connection_name: [
            { required: true, message: '请输入连接名称', trigger: 'change' }
          ],
          database_type: [
            { required: true, message: '请输入数据库类型', trigger: 'change' }
          ],
          database_version: [
            { required: true, message: '请输入数据库版本', trigger: 'change' }
          ],
          host: [
            { required: true, message: '请输入主机名/IP', trigger: 'change' }
          ],
          port: [
            { required: true, message: '请输入端口', trigger: 'change' }
          ],
          database_name: [
            { required: true, message: '请输入数据库名', trigger: 'change' }
          ],
          charset: [
            { required: true, message: '请输入字符集', trigger: 'change' }
          ],
          username: [
            { required: true, message: '请输入用户名', trigger: 'change' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'change' }
          ],
          connection_url: [
            { required: true, message: '请输入数据库链接地址', trigger: 'change' }
          ],
          enabled: [
            { required: true, message: '请选择是否启用', trigger: 'change' }
          ]
        },
        columns: [
          {
            prop: 'connection_name',
            label: '连接名称',
            minWidth: 250
          },
          {
            prop: 'database_type',
            label: '数据库类型',
            minWidth: 100
          },
          {
            prop: 'database_version',
            label: '数据库版本',
            minWidth: 100
          },
          {
            prop: 'host',
            label: '主机名/IP',
            minWidth: 100
          },
          {
            prop: 'port',
            label: '端口',
            minWidth: 100
          },
          {
            prop: 'database_name',
            label: '数据库名',
            minWidth: 100
          },
          {
            prop: 'charset',
            label: '字符集',
            minWidth: 100
          },
          {
            prop: 'username',
            label: '用户名',
            minWidth: 100
          },
          {
            prop: 'connection_url',
            label: '数据库链接地址',
            minWidth: 130
          },
          {
            prop: 'enabled',
            label: '是否启用',
            minWidth: 100
          },
          {
            prop: 'valid',
            label: '是否有效',
            minWidth: 100,
            formatter: (row, column, cellValue, index) => {
              return cellValue === 1 ? '有效' : '无效'
            }
          },
          // {
          //   prop: 'version',
          //   label: '版本号',
          //   minWidth: 100
          // },
          {
            prop: 'remark',
            label: '备注',
            minWidth: 100
          },
          {
            prop: 'create_by',
            label: '创建人',
            minWidth: 100
          },
          {
            prop: 'create_at',
            label: '创建时间',
            minWidth: 160
          },
          {
            prop: 'update_by',
            label: '更新人',
            minWidth: 100
          },
          {
            prop: 'update_at',
            label: '更新时间',
            minWidth: 160
          }
        ],
        searchForm: {
          keyword: '',
          page: 1,
          page_size: 10
        }
      }
    },
    mounted() {
      this.getList()
    },
    methods: {
      // 编辑
      onEdit(data) {
        this.visibleDialog = true
        this.form = { ...data }
      },
      // 删除
      onDel(id) {
         this.$confirm('此操作将删除该数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          const params = {
            ids: [id]
          }
          del(params).then(res => {
            if (res.code === 200) {
              this.$message.success('删除成功')
              this.getList()
            }
          })
        }).catch(() => {
        })
      },
      // 状态
      onEditStatus(id, enabled) {
        const msg = enabled ? '启用' : '停用'
        enabled = enabled ? 1 : 0
        this.$confirm(`此操作将${msg}该数据, 是否继续?`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          editStatus({ ids: [id], enabled }).then(res => {
            if (res.code === 200) {
              this.$message.success(msg + '成功')
              this.getList()
            }
          })
        }).catch(() => {
        })
      },
      // 提交
      onSubmit() {
        this.$refs['form'].validate((valid) => {
          if (valid) {
            if (this.form.id) {
              edit(this.form).then(res => {
                if (res.code === 200) {
                  this.visibleDialog = false
                  this.getList()
                }
                this.loading = false
              })
            } else {
              add(this.form).then(res => {
                if (res.code === 200) {
                  this.visibleDialog = false
                  this.getList()
                }
                this.loading = false
              })
            }
          } else {
            console.log('error submit!!')
            return false
          }
        })
      },
      // 关闭
      onClose() {
        this.form = {
          connection_name: '',
          database_type: '',
          database_version: '',
          host: '',
          port: '',
          database_name: '',
          charset: '',
          username: '',
          password: '',
          connection_url: '',
          enabled: 1,
          remark: ''
        }
        this.$refs.form.resetFields()
      },
      // 切换页面大小
      onChangePageSize(page_size) {
        this.searchForm.page_size = page_size
        this.getList()
      },
      // 切换页面
      onChangePage(page) {
        this.searchForm.page = page
        this.getList()
      },
      // 获取表数据
      getList() {
        this.dataList = []
        this.loading = true
        getList(this.searchForm).then(res => {
          if (res.code === 200) {
            this.dataList = res.data.items
            this.total = res.data.total
          }
          this.loading = false
        })
      },
      // 新增
      onAdd() {
        this.visibleDialog = true
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

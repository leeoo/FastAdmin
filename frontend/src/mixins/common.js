export default {
  data() {
    return {
      loading: false,
      total: 0, // 分页总数
      dataList: [], // 数据列表
      columns:[],
      form: {
        page_no: 1,
        page_size: 10
      }
    }
  },
  mounted(){
  },
  methods:{
    // 切换页面大小
    onChangePageSize(page_size){
      this.form.page_size = page_size
      this.getList()
    },
    // 切换页面
    onChangePage(page_no){
      this.form.page_no = page_no
      this.getList()
    },
    // 获取表数据
    getList(){
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
                columns.push({
                  prop: arr[0],
                  label: arr[1] ||　'#'
               })
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
<template>
  <div class="container">
      <GoodsCategoryList></GoodsCategoryList>
  </div>
</template>

<script>
  import GoodsCategoryList from './compoent/GoodsCategoryList'

  export default {
    name: 'Index',
    components: {
      GoodsCategoryList
    },
    data() {
      return {
        showGoodsList: true,
        modifyGoodsId: null
      }
    },
    methods: {
    }
  }
</script>

<style lang="scss" scoped>
  .container {
    padding: 20px;
    min-height: 100vh;
    background-color: rgb(240, 242, 245);

    .box-wrapper {
      background-color: #fff;
      border-radius: 3px;
      padding: 20px;
    }
  }

</style>

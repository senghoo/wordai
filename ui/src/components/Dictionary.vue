<template>
<div class="main">
  <div class="dict-head">
    <span>{{word}}</span>
  </div>
  <el-collapse v-model="activeName" accordion>
    <el-collapse-item v-for="desc in define" :name="desc.seq">
      <template slot="title">
        <el-tag size="mini">{{desc.speech}}</el-tag>
        <span class="en">{{desc.cn}}</span>
      </template>
      <div>{{desc.en}}</div>
      <div v-for="eg in desc.examples">
        <el-divider content-position="left">例句</el-divider>
        <div>{{eg.en}}</div>
        <div>{{eg.cn}}</div>
      </div>
    </el-collapse-item>
  </el-collapse>
</div>
</template>

<script>
export default {
  name: 'Main',
  mounted (){
    this.load_dict()
  },
  computed: {
  },
  data () {
    return {
      start: 0,
      define: [],
      activeName: '1'
    }
  },
  props: {
    word: ''
  },
  watch: {
    word () {
      this.load_dict()
    }
  },
  methods: {
    load_dict (){
      this.axios({
        "method": "GET",
        "url": "/dictionary/"+this.word
      }).then(res => {
        this.star = res.data.star
        this.define = res.data.descriptions
      }, err=>{
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style rel="stylesheet/scss" lang="scss" scoped>
.dict-head{
  text-align: left;
  font-size: 2em;
  background: #C1D5D6;
  padding: 5px;
}
.answer{
  margin: 30px;
}
.card {
  margin:100px auto;
  width:500px;
  background-color: white;
  min-height: 250px;
  border-radius: .5rem;
  box-shadow: 0 3px 0.5rem #d9d9d9;
  .quiz {
    margin: 10px 30px;
  }
  .en {
    font-size: 2rem;
  }
}
.main{
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.en{
  line-height: 13px;
  padding: 5px 10px;
  align-items: flex-start;
  overflow: hidden;
}
</style>

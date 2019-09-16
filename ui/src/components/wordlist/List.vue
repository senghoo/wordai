<template>
  <div>
<div class="wordlist" v-if="show=='list'">
  <el-button type="primary" icon="el-icon-edit" size="mini" @click="create">新建</el-button>
  <el-table
    :data="lists"
    style="width: 100%">
    <el-table-column
      label="名称"
      prop="name">
    </el-table-column>
    <el-table-column
      label="单词数"
      prop="words"
      :formatter="formatWordCount">
    </el-table-column>
    <el-table-column
      prop="user"
      label="类型"
      width="100">
      <template slot-scope="scope">
        <el-tag
          :type="scope.row.user ?  'success' : 'primary'"
          disable-transitions>{{scope.row.user ?  '用户' : '系统'}}</el-tag>
      </template>
    </el-table-column>
    <el-table-column
      align="right">
      <template slot-scope="scope">
        <el-button
          v-if="scope.row.user"
          type="text"
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
        <el-button
          v-if="scope.row.user"
          type="text danger"
          size="mini"
          @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
      </template>
    </el-table-column>
  </el-table>
</div>
<div class="wordlist" v-if="show=='form'">
  <wordlist-form
    v-model="formId"
    @cancel="formCancel"
    @submit="formSubmit"
    >
  </wordlist-form>
</div>
</div>
</template>
<script>
import WordlistForm from './Form'
export default {
  components: {
    WordlistForm
  },
  mounted (){
    this.load_list()
  },
  data () {
    return {
      formId: null,
      show: 'list',
      lists: [],
      selected: {}
    }
  },
  methods: {
    formCancel(){
      this.formId = null
      this.show = 'list'
      this.load_list()
    },
    formSubmit(){
      this.formId = null
      this.show = 'list'
      this.load_list()
    },
    handleEdit(idx, row){
      this.formId = row.id
      this.show = 'form'
    },
    handleDelete(idx, row){
      this.axios({
	      'method': 'DELETE',
	      'url': '/wordlist/'+row.id,
      }).then(res=>{
        this.$message({
          message: '删除成功',
          type: 'success'
        })
        this.load_list()
      }, err=>{
        this.$message({
          message: '您无权访问此单词表',
          type: 'warning'
        })
        this.load_list()
      })
    },
    create(){
      this.selected = {}
      this.show='form'
    },
    load_list(){
      return this.axios({
        'method': 'GET',
        'url': '/wordlist'
      }).then(res=>{
        this.lists = res.data
      })
    },
    formatWordCount(row){
      return row.words.length
    }
  }
}
</script>

<style lang="scss" scoped>
ul{
  max-height: 500px;
}
</style>

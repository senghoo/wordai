<template>
<el-form :model="form">
  <el-form-item label="单词本" :label-width="'70px'">
    <el-select v-model="form.wordlist" placeholder="请选择活动区域">
      <el-option v-for="item in lists" :label="item.name" :value="item.id"></el-option>
    </el-select>
  </el-form-item>
</el-form>
</template>
<script>
export default {
  mounted (){
    this.load_current()
    this.load_list()
  },
  data () {
    return {
      form: {
        wordlist: '',
      },
      lists: []
    }
  },
  methods: {
    load_current(){
      return this.axios({
	      'method': 'GET',
	      'url': '/user/wordlist',
      }).then(res=>{
        this.form.wordlist = res.data.wordlist
      })
    },
    load_list(){
      return this.axios({
	      'method': 'GET',
	      'url': '/wordlist'
      }).then(res=>{
        this.lists = res.data
      })
    },
    submit(){
      return this.axios({
	      'method': 'POST',
	      'url': 'http://127.0.0.1:8000/api/user/wordlist',
	      'data': this.form
      })
    }
  }
}
</script>

<style lang="scss" scoped>
ul{
  max-height: 500px;
}
</style>

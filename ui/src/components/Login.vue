<template>
<div class="login">
<el-row>
  <el-col :span="24">
    <el-input id="name"  v-model="name" placeholder="请输入帐号">
      <template slot="prepend">帐号</template>
    </el-input>
  </el-col>
</el-row>
<el-row>
  <el-col :span="24">
    <el-input id="password" v-model="password" type="password" placeholder="请输入密码" @keyup.enter.native="login">
      <template slot="prepend">密码</template>
    </el-input>
  </el-col>
</el-row>
<el-row>
  <el-col :span="24">
    <el-button id="login" v-on:click="login" style="width:100%" type="primary">登录</el-button>
  </el-col>
</el-row>
</div>
</template>
<script>
import { mapGetters, mapActions } from 'vuex'
export default {
  data() {
    return {
      name: '',
      password: '',
      passwordErr: false
    }
  },
  computed: {
    ...mapGetters([
      'username',
    ])
  },
  methods: {
    ...mapActions([
      `fetchJWT`
    ]),
    login() {
      this.fetchJWT({
        // #Security...
        username: this.name,
        password: this.password
      }).then(()=>{
        this.$router.push({ path: '/' })
      }, (err)=>{
        console.log(err)
        this.$message({
          message: '用户名密码错误',
          type: 'warning'
        });
      })
    }
  },

  mounted() {
  }
}
</script>
<style rel="stylesheet/scss" lang="scss" scoped>
.login {
  margin:20% auto;
  width:300px;
}
.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
</style>

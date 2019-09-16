<template>
<div class="main">
  <div class="content">
  <el-menu  class="right-menu" :collapse="true" active-text-color="#303133">
    <el-submenu index="1">
      <template slot="title">
        <i class="el-icon-notebook-2"></i>
        <!-- <i class="el-icon-list-alt"></i> -->
        <span slot="title">单词表</span>
      </template>
      <el-menu-item-group>
        <span slot="title">单词表</span>
        <el-menu-item index="1-1" @click="openLearned">已学单词</el-menu-item>
        <el-menu-item index="1-2" @click="openToLearn">未学单词</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="2" @click="openStatistic">
      <i class="el-icon-s-marketing"></i>
      <span slot="title">统计数据</span>
    </el-menu-item>
    <el-menu-item index="3" >
      <i class="el-icon-reading" @click="openWordlistList"></i>
      <span slot="title">单词本</span>
    </el-menu-item>
    <el-menu-item index="4" @click="settingVisible = true">
      <i class="el-icon-setting"></i>
      <span slot="title">设置</span>
    </el-menu-item>
  </el-menu>
  <el-row>
    <el-col :sm="{span: 18, offset: 3}" :md="{span: 12, offset: 6}" class="card" >
      <card ref="card" v-on:correct="onCorrect" v-on:wrong="onWrong"></card>
    </el-col>
  </el-row>
  </div>

  <el-dialog title="单词本" :visible.sync="wordlistListVisible" width="90%" class="wordlist-list" custom-class="wordlist-list-2">
    <wordlist-list ref="wordlistList"> </wordlist-list>
  </el-dialog>
  <el-dialog title="设置" :visible.sync="settingVisible">
    <wordlist-setting ref="wordlistSetting"> </wordlist-setting>
    <div slot="footer" class="dialog-footer">
      <el-button @click="settingVisible = false">取 消</el-button>
      <el-button type="primary" @click="settingSubmit">确 定</el-button>
    </div>
  </el-dialog>
  <el-dialog
    title="统计信息"
    :visible.sync="statisticVisible"
    width="80%"
    center>
    <statistic ref="statistics"></statistic>
    <span slot="footer" class="dialog-footer">
      <el-button @click="statisticVisible = false">关 闭</el-button>
    </span>
  </el-dialog>
  <el-drawer class="right-drawer"
             title="单词表 "
             custom-class="right-drawer"
             :visible.sync="showWordlist"
             size="250"
             direction="rtl">
    <wordlist ref="wordlist" class="wordlist"></wordlist>
  </el-drawer>
  <el-drawer class="bottom-drawer"
             title="词典"
             custom-class="dict-drawer"
             :visible.sync="showDict"
             :modal="false"
             direction="btt">
      <dictionary :word="word"></dictionary>
  </el-drawer>
</div>
</template>

<script>
import 'element-ui/lib/theme-chalk/display.css';
import Dictionary from './Dictionary'
import Card from './Card'
import wordlist from './wordlist'
import WordlistSetting from './wordlist/Setting'
import WordlistList from './wordlist/List'
import statistic from './statistic'
export default {
  name: 'Main',
  components: {
    Dictionary,
    Card,
    wordlist,
    WordlistSetting,
    WordlistList,
    statistic
  },
  mounted (){},
  data () {
    return {
      showDict: false,
      word:"",
      showWordlist: false,
      settingVisible: false,
      statisticVisible: false,
      wordlistListVisible: false
    }
  },
  methods: {
    openWordlistList(){
      this.wordlistListVisible = true
    },
    openStatistic(){
      this.statisticVisible = true
      this.$refs.statistics.load()
    },
    openLearned(){
      this.showWordlist = true

      this.$nextTick(() => {
        this.$refs.wordlist.openLearned()
      })
    },
    openToLearn(){
      this.showWordlist = true
      this.$nextTick(() => {
        this.$refs.wordlist.openToLearn()
      })
    },
    onWrong(word) {
      this.word = word
      this.showDict = true
      this.$message({
        message: '回答错误',
        type: 'warning'
      })
    },
    onCorrect() {
      this.word = ""
      this.showDict = false
      this.$message({
        message: '回答正确，继续努力!!',
        type: 'success'
      })
    },
    settingSubmit() {
      var self = this
      this.$refs.wordlistSetting.submit().then(()=>{
        self.$refs.card.load_quiz()
        self.settingVisible = false
        self.$message({
          message: '设置成功',
          type: 'success'
        })
      })
    }
  }
}
</script>

<style lang="scss">
  .dict-drawer{
  overflow-y: scroll;
  #el-drawer__title{
  padding: 5px 10px;
    margin: 0;
  }
  }
</style>
<style lang="scss" scoped>
  .content{
  margin: 5px;
  }

  .right-menu{
  position: fixed;
  bottom: 20px;
  right: 5px;
  }

  .content{
  padding-top: 20px;
  }
  @media(min-width: 768px){
  .content{
  padding-top: 20vh;
  }

  .right-menu{
  position: absolute;
  z-index:100;
  bottom: initial;
  right: initial;
  }
  }
  .main{
  height: 100%;
  }
  .top-padding{
  height: 20%;
  }
  .card {
  background-color: white;
  min-height: 250px;
  border-radius: .5rem;
  box-shadow: 0 3px 0.5rem #d9d9d9;
  }
  .dict {
  width: 800px;
  margin: 0 auto;
  overflow: hidden;
  }
  .right-drawer{
  max-height: 100%;
  .right-drawer-body{
  max-height: 100%;
  min-width:300px;
  }
  }
  .wordlist{
  height: 500px;
}
  </style>

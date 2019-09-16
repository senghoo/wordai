<template>
  <el-tabs v-model="activeName"  class="tabs">
    <el-tab-pane label="已学单词" name="learned">
      <learned ref="learned" class="words"></learned>
    </el-tab-pane>
    <el-tab-pane label="未学单词" name="tolearn">
      <to-learn ref="toLearn" class="words"></to-learn>
    </el-tab-pane>
  </el-tabs>
</template>
<script>
import Learned from './Learned'
import ToLearn from './ToLearn'

export default {
  components: {
    Learned,
    ToLearn
  },
  data() {
    return {
      activeName: 'learned'
    };
  },
  methods: {
    openLearned(){
      this.$refs.learned.load()
      this.$refs.toLearn.load()
      this.activeName = 'learned'
    },
    openToLearn(){
      this.$refs.learned.load()
      this.$refs.toLearn.load()
      this.activeName = 'tolearn'
    },
  }
}
</script>

<style lang="scss" scoped>
  .tabs {
  margin: 0 20px;
}
</style>

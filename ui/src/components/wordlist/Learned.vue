<template>
<el-timeline>
    <el-timeline-item
      v-for="(activity, index) in learned"
      :key="activity.wordname"
      :type="tp(activity)"
      size="large"
      color="color"
      :timestamp="ts(activity)">
      {{activity.wordname}}
    </el-timeline-item>
  </el-timeline>
</template>
<script>
export default {
  mounted () {
    this.load()
  },
  data () {
    return {
      // now: new Date(),
      learned: []
    }
  },
  methods: {
    load () {
      this.axios({
        'method': 'GET',
        'url': '/wordlist/learned'
      }).then(res=>{
        this.learned = res.data
      })
    },
    needReview(act){
      var now = this.$moment()
      var review = this.$moment(act.review)
      return review.isBefore(now)
    },
    tp (act){
      if (this.needReview(act)){
        return 'danger'
      } else {
        return 'success'
      }
    },
    ts (act) {
      var prefix='预计复习: '
      if (this.needReview(act)){
        prefix = '记忆过期：'
      }
      return prefix + this.$moment(act.review).tz("Asia/Shanghai").fromNow()
    }
  }
}
</script>

<style lang="scss" scoped>
  ul{
  max-height: 500px;
  }
</style>

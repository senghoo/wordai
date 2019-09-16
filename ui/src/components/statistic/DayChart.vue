<template>
  <div>
    <div id="day_chart_echart" style="height: 400px; width: 100%;"></div>
  </div>
</template>
<script>
var echarts = require('echarts');
export default {
  mounted () {
    this.load_data();
  },
  data () {
    return {
      // now: new Date(),
      data: {
        exercise: {},
        review: {}
      }
    }
  },
  computed:{
    xaxis() {
      var res = []
      return this.$_.sortBy(
        this.$_.uniq(this.$_.union(
          this.$_.keys(this.data.exercise),
          this.$_.keys(this.data.review))),
        a=>{a}
      )
      return res
    },
    yaxis(){
      return [
        {name: '已学', type: 'line', data: this.$_.map(this.xaxis, date=>{
          return this.data.exercise[date] ? this.data.exercise[date] : 0
        })},
        {name: '需要复习', type: 'line', data: this.$_.map(this.xaxis, date=>{
          return this.data.review[date] ? this.data.review[date] : 0
        })}
      ]
    }
  },
  methods: {
    load_data(){
      this.axios({
	      "method": "GET",
	      "url": "/statistic/learn",
      }).then(res=>{
        this.data = res.data
        this.init_echarts()
      })
    },
    init_echarts () {
      // 基于准备好的dom，初始化echarts实例
      var echart_etl_stat = echarts.init(document.getElementById('day_chart_echart'));
      // 设置option
      var echart_etl_stat_option = {
          title: {
              text: '学习数量'
          },
          tooltip: {
              trigger: 'axis'
          },
          legend: {
              data:['已学', '需要复习'  ]
          },
          grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
          },
          xAxis: {
              type: 'category',
              boundaryGap: false,
              data: this.xaxis
          },
          yAxis: {
              type: 'value'
          },
          series: this.yaxis
      };
      // 绘制图表
      echart_etl_stat.setOption(echart_etl_stat_option);
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

<template>
<div>
  <el-row>
    <el-col :span="24">
      <day-chart ref="dayChart"></day-chart>
    </el-col>
  </el-row>
</div>
</template>
<script>
import DayChart from './DayChart'

export default {
  components: {
    DayChart,
  },
  data() {
    return {
    };
  },
  methods: {
    load(){
      this.$refs.dayChart.load()
    }
  }
}
</script>

<style lang="scss" scoped>
</style>

<template>
  <div class="list-container">
    <ul class="infinite-list" v-infinite-scroll="load" style="overflow:auto">
      <li v-for="i in to_learn" class="infinite-list-item">
        <span class="word">{{i}}</span>
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  data () {
    return {
      now: new Date(),
      to_learn: []
    }
  },
  methods: {
    load () {
      this.axios({
        'method': 'GET',
        'url': '/wordlist/to_learn'
      }).then(res=>{
        this.to_learn = res.data
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

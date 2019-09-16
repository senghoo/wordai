<template>
  <div class="card" v-if="!alldone">
    <div class="cn" >
      <span>{{quiz.cn}}</span>
    </div>
    <div class="quiz">
      <span class="en">{{quiz.cloze}}</span>
    </div>
    <el-form label-width="50px" class="answer">
      <el-form-item v-for="(ans, idx) in answers" label="答案">
        <el-input v-model="answers[idx]"
                  @keydown.enter.native="submitAnswer"
                  @keydown.tab.native="(event)=>{tabEvent(event, idx)}"
                  @keydown.space.native="(event)=>{spaceDownEvent(event, idx)}"
                  @keyup.space.native="(event)=>{spaceUpEvent(event, idx)}"
                  autocomplete="off"
                  autocorrect="off"
                  autocapitalize="off"
                  spellcheck="false"
                  :ref="'answer-'+idx" >
          <div slot="suffix">
            <el-tooltip v-model=showAns[idx] :content="quiz.answers[idx]" effect="light" placement="right">
              <span> 查看答案</span>
            </el-tooltip>
          </div>
        </el-input>
      </el-form-item>
    </el-form>
  </div>
  <div v-else>
    <el-row>
      <span>您已经完成所有字卡。</span>
    </el-row>
  </div>
</template>

<script>
import Dictionary from './Dictionary'
export default {
  name: 'Main',
  components: {
    Dictionary
  },
  mounted (){
    this.load_quiz()
  },
  data () {
    return {
      showAns:{},
      showDict: false,
      quiz: {},
      answers: [],
      alldone: false
    }
  },
  methods: {
    load_quiz (){
      this.showDict = false
      this.axios({
	      "method": "GET",
	      "url": "/learn/word"
      }).then(res => {
        this.quiz = res.data
        this.cleanAnswer()
        this.$nextTick(() => {
          this.focusAnswer(0)
        })
      }, err=>{
        if (err.response.status == 404) {
          this.alldone = true
        }
      })
    },
    cleanAnswer(){
      this.answers = []
      for (var i = 0; i < this.quiz.check.length; i++) {
        this.answers.push('')
      }
    },
    focusAnswer(idx){
      this.$refs["answer-"+idx][0].focus()
    },
    submitAnswer() {
      this.axios({
	      'method': 'POST',
	      'url': '/learn/word',
	      'data': {
		      'check': this.quiz.check,
		      'id': this.quiz.id,
		      'sid': this.quiz.sid,
		      'answers': this.answers
        }
      }).then(res => {
        if (res.data.result) {
          this.load_quiz()
          this.$emit('correct', this.quiz.word)
        } else {
          this.cleanAnswer()
          this.$emit('wrong', this.quiz.word)
        }
      })
    },
    tabEvent(event, idx){
      if (this.answers.length > idx+1){
        this.focusAnswer(idx+1)
    }else{

      this.focusAnswer(0)
    }
      event.preventDefault()
    },
    spaceDownEvent(event, idx){
      this.showAns[idx] = true
      event.preventDefault()
    },
    spaceUpEvent(event, idx){
      this.showAns[idx] = false
      event.preventDefault()
    }
  }
}
</script>

<style lang="scss" scoped>
  .cn{
  padding:20px 20px 0px 20px;
  }
  .quiz{
  padding:5px 20px 20px 20px;
  font-size: 1.5em;
  }
  .answer{
  padding: 0px 20px 20px 20px;
  }
</style>

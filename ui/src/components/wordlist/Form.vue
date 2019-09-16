<template>
<el-form :model="form" label-width="80px">
  <el-form-item label="名称">
    <el-input v-model="form.name"></el-input>
  </el-form-item>
  <el-form-item label="描述">
    <el-input v-model="form.description"></el-input>
  </el-form-item>
  <label class="wl-label" >单词列表:</label>
  <div class="wl-border">
    <div class="wl-container">
      <div class="wl-backdrop" ref="backdrop">
        <div class="wl-highlights" v-html="highlight"></div>
      </div>
      <textarea ref="textInput" class="wl-input" v-model="wordText"
                autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"
                @keydown.enter="load_define"
                @blur="load_define"
                ></textarea>
    </div>
  </div>
  <br/>
  <el-form-item>
    <el-button type="primary" @click="submit">提交</el-button>
    <el-button @click="cancel">取消</el-button>
  </el-form-item>
</el-form>
</template>
<script>
export default {
  mounted (){
    this.load_word()
    this.$refs.textInput.addEventListener('scroll', () => {
      this.$refs.backdrop.scrollTop = this.$refs.textInput.scrollTop
    }, false)
  },
  data () {
    return {
      wordText: '',
      form: {
        name: '',
        description: '',
      },
      checkRes: {
        defines: {},
        not_dict: [],
        not_sentence: []
      }
    }
  },
  props: {
    value: ''
  },

  watch: {
    value () {
      this.load_word()
    }
  },
  computed: {
    words() {
      return this.$_.uniq(this.$_.reject(
        this.$_.map(
          this.wordText.split("\n"),
          w=>{
            return w.trim()
          }
        ), word=>{
          return !word || word === ''
        }))
    },
    highlight(){
      var texts = this.wordText
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;")
          .replace(/"/g, "&quot;")
          .replace(/'/g, "&#039;").split("\n")
      return this.$_.map(texts, l=>{
        var w = l.trim()
        var define = this.checkRes.defines[w]
        if (define){
          return '<div class="wl-line-div"><span class="highlight-word">' + l +'</span> <span class="desc">'+define.descriptions[0].description+'</span></div>'
        } else if (w ==='') {
          return l
        } else {
          return '<div class="wl-line-div"><span class="highlight-word-ne">' + l +'</span> <span class="desc">未找到定义或例句</span></div>'
        }
      }).join('')
    }
  },
  methods: {
    cancel() {
      this.$emit('cancel')
    },
    load_word() {
      this.clean()
      if (this.value){
        this.axios({
	        'method': 'GET',
	        'url': '/wordlist/'+this.value,
        }).then(res=>{
          this.form.name = res.data.name
          this.form.description = res.data.description
          this.wordText = res.data.words.join('\n')
          this.load_define()
        }, err=>{
          this.$message({
            message: '您无权访问此单词表',
            type: 'warning'
          })
          this.cancel()
        })
      }
    },
    clean(){
      this.form.name =''
      this.form.description = ''
      this.wordText = ''
      this.checkRes =  {
        defines: {},
        not_dict: [],
        not_sentence: []
      }
    },
    submit() {
      if (!this.value){
        this.axios({
          'method': 'POST',
          'url': '/wordlist',
          'data': {
            'name': this.form.name,
            'description': this.form.description,
            'words': this.words
          }
        }).then(res=>{
          this.$emit('submit')
        })
      } else {
        this.axios({
          'method': 'PUT',
	        'url': '/wordlist/'+this.value,
          'data': {
            'name': this.form.name,
            'description': this.form.description,
            'words': this.words
          }
        }).then(res=>{
          this.$emit('submit')
        })
      }
    },
    load_define(){
      this.axios({
        'method': 'PUT',
        'url': '/wordlist',
        'data': this.words
      }).then(res=>{
        this.checkRes = res.data
      })
    }
  }
}
</script>

<style lang="scss">
.wl-container, .wl-backdrop, .wl-input {
  width: 100%;
  height: 180px;
}
.wl-highlights, .wl-input {
  font-family: Consolas,Liberation Mono,Courier,monospace;
  letter-spacing: 1px;
  font-size: 14px; word-wrap: break-word;
}
.wl-border{
  border: 1px solid;
}
.wl-container {
  display: block;
  margin: 0 auto;
  transform: translateZ(0);
  -webkit-text-size-adjust: none;
  padding:1px;

}
.wl-backdrop {
  position: absolute;
  z-index: 1;
  background-color: #fff;
  overflow: auto;
  pointer-events: none;
  transition: transform 1s;
}

.wl-highlights {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: transparent;
  /* color: red; */
}
.wl-input {
  display: block;
  position: absolute;
  z-index: 2;
  margin: 0;
  border: 2px solid #74637f;
  border-radius: 0;
  color: #444;
  background-color: transparent;
  overflow: auto;
  resize: none;
  transition: transform 1s;
  padding:0;
  border-style: none;
}
.wl-line-div{
  overflow: visible;
  white-space: nowrap;
  height:16px;
}
.highlight-word{
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.highlight-word-ne{
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  border-radius: 3px;
  color: transparent;
  border-bottom:1px solid red;
}
.desc{
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  overflow-y: vi;
  white-space: nowrap;
  color: gray;
  font-size: 12px;

}


mark {
  color: transparent;
  background-color: #d4e9ab; /* or whatever */
}

textarea {
  margin: 0;
  border-radius: 0;
}
textarea:focus, button:focus {
  outline: none;
  box-shadow: 0 0 0 2px #c6aada;
}
</style>

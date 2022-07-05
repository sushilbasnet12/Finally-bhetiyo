

console.log('hello')
Vue.createApp({

    delimiters: ["[[", "]]"],
    data() {
        return {
            message: 'Hello Vue!'
        }
    }
}).mount('#app')
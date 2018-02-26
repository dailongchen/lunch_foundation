// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'

Vue.config.productionTip = false
Vue.use(VueRouter)

var router = new VueRouter({
  routes: [
    { path: '/', component: App.components.Summary },
    { path: '/SubmitExpense', component: App.components.SubmitExpense }
  ]
})

/* eslint-disable no-new */
new Vue({
  router,
  el: '#app',
  template: '<App/>',
  components: { App }
})

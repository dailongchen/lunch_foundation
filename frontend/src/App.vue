<template>
  <div id="app" style="margin: 5%;">
    <div class="container">
      <router-link to="/"><img src="./assets/logo.png"></router-link>

      <h2>Have Fun on your Lunch Break</h2>
      <h5>by Mozy Native Client team (ShangHai)</h5>

      <router-view/>
    </div>
  </div>
</template>

<script>
import Summary from './components/Summary'
import SubmitExpense from './components/SubmitExpense'

export default {
  name: 'app',
  components: {
    Summary,
    SubmitExpense
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

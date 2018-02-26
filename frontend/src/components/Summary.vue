<template>
  <div>
    <router-link to="/SubmitExpense">
      <button type="button" class="btn btn-primary">Submit Expense</button>
    </router-link>

    <br/>
    <h4 style="color:red">{{ error_message }}</h4>
    <br/>

    <h3>余额</h3>
    <table class="table">
      <thead class="thead-dark">
        <tr>
          <th v-for="member in members" v-if="!member.hidden">
            {{ member.name }}
          </th>
          <th>总计</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th v-for="member in members" v-if="!member.hidden">
            {{ member.remaining }}
          </th>
          <th>{{ total_remaining }}</th>
        </tr>
      </tbody>
    </table>

    <div class="form-check form-check-inline" v-on:click="showLast">
      <label class="form-check-label">
        <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1" checked> 最近
      </label>
    </div>
    <div class="form-check form-check-inline" v-on:click="showThisWeek">
      <label class="form-check-label">
        <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="option2"> 本周
      </label>
    </div>
    <div class="form-check form-check-inline" v-on:click="showThisMonth">
      <label class="form-check-label">
        <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="option3"> 本月
      </label>
    </div>

    <div v-for="oneEvent in events">
      <br/>

      <div v-if="oneEvent.event.restaurant.length > 0">
        <h3>
          <span style="color:blue">
            {{ oneEvent.event.restaurant }}
          </span>
          <span style='font-size: medium;'>
            {{ oneEvent.event.time }}
          </span>
        </h3>
      </div>
      <div v-else>
        <h3>
          <span style="color:blue">
            充值
          </span>
          <span style='font-size: medium;'>
            {{ oneEvent.event.time }}
          </span>
        </h3>
      </div>

      <table class="table">
        <thead>
          <tr>
            <th v-for="cost in oneEvent.costs">
              {{ cost.member.name }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th v-for="cost in oneEvent.costs">
              <div v-if="oneEvent.event.restaurant.length > 0">
                {{ cost.cost }}
              </div>

              <div v-if="cost.recharge > 0">
                <div v-if="oneEvent.event.restaurant.length > 0">
                  (+{{ cost.recharge }})
                </div>
                <div v-else>
                  +{{ cost.recharge }}
                </div>
              </div>
            </th>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Summary',
  data () {
    return {
      events: [],
      members: [],
      error_message: ''
    }
  },
  computed: {
    total_remaining: function () {
      return this.members.reduce(function (total, item) {
        return total + parseFloat(item.remaining)
      }, 0).toFixed(2)
    }
  },
  methods: {
    showLast: function () {
      axios.get('/lunch_foundation/last', { params: { n: 3 } })
      .then((response) => {
        this.events = response.data.result
      }, (error) => {
        this.error_message = error.message
      })
    },
    showThisWeek: function () {
      axios.get('/lunch_foundation/this_week')
      .then((response) => {
        this.events = response.data.result
      }, (error) => {
        this.error_message = error.message
      })
    },
    showThisMonth: function () {
      axios.get('/lunch_foundation/this_month')
      .then((response) => {
        this.events = response.data.result
      }, (error) => {
        this.error_message = error.message
      })
    }
  },
  mounted () {
    this.showLast()

    axios.get('/lunch_foundation/members')
    .then((response) => {
      this.members = response.data.result
    }, (error) => {
      this.error_message = error.message
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
h3, h6 {
  text-align: left;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

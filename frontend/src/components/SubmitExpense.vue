<template>
  <div>
    <br/>
    <h4 style="color:red">{{ error_message }}</h4>
    <br/>

    <div align="left">
      <div class="form-group">
        <label for="restaurantInput">饭店</label>
        <input class="form-control" id="restaurantInput" placeholder="输入饭店名, 充值请留空白" v-model="restaurant">
      </div>
      <div class="form-group">
        <label for="timeInput">时间</label>
        <input class="form-control" id="timeInput" type="date" placeholder="例: 2018-01-30" v-model="eventTime">
      </div>
      <div class="form-group">
        <label for="totalExpenseInput">总支出</label>
        <input class="form-control" id="totalExpenseInput" type="number"
               v-model.number="costSum"
               :disabled="restaurant.length == 0">

        <div class="form-check form-check-inline">
          <label class="form-check-label" for="AA">
            <input class="form-check-input" type="radio" id="AA" value="AA"
                   v-model="payMode"
                   :disabled="restaurant.length == 0"> 平摊
          </label>
        </div>
        <div class="form-check form-check-inline">
          <label class="form-check-label" for="NotAA">
            <input class="form-check-input" type="radio" id="NotAA" value="Not-AA"
                   v-model="payMode"
                   :disabled="restaurant.length == 0"> 各付各
          </label>
        </div>
      </div>

      <table class="table">
        <thead class="thead-dark">
          <tr>
            <th class="w-10"></th>
            <th class="w-10">消费</th>
            <th class="w-10">充值</th>
            <th class="w-25">余额</th>
          </tr>
        </thead>
        <tbody align="left">
          <tr v-for="member in members" v-if="!member.hidden">
            <th>
              <label>
                <input type="checkbox" :value="member.name" v-model="checkedNames">
                {{ member.name }}
              </label>
            </th>
            <th>
              <label v-if="payMode === 'AA'">{{ member.cost.toFixed(2) }}</label>
              <input class="form-control"
                     v-model.number="member.cost"
                     v-if="payMode !== 'AA'"
                     :disabled="restaurant.length == 0 || !checkedNames.includes(member.name)">
            </th>
            <th>
              <input class="form-control"
                     v-model.number="member.recharge"
                     :disabled="!checkedNames.includes(member.name)">
            </th>
            <th>
              {{ getNewRemaining(member) }}
              <span style="color:blue" v-if="checkedNames.includes(member.name)">(原值：{{ member.remaining }}）</span>
            </th>
          </tr>
        </tbody>
      </table>

    </div>

    <div align="right">
      <h4 style="color:red" v-if="submit_error_message.length > 0">{{ submit_error_message }}</h4>
      <label>
        总额支出: {{ foundationCost.toFixed(2) }}, 充值: {{ foundationRecharge.toFixed(2) }}, 新总额: {{ newTotalRemaining.toFixed(2) }}
        <span style="color:blue">(原值：{{ totalRemaining.toFixed(2) }}）</span>
      </label>
      <button type="button" class="btn btn-primary" v-on:click="submitNewExpense()">OK</button>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubmitExpense',
  data () {
    return {
      members: [],
      payMode: 'AA',
      restaurant: '',
      eventTime: new Date().toISOString().slice(0, 10),
      costSum: 0.0,

      checkedNames: [],

      error_message: '',
      submit_error_message: ''
    }
  },
  watch: {
    payMode: function (val) {
      this.resetCosts()
    },
    checkedNames: function (val) {
      if (this.payMode === 'AA') {
        this.setToAA()
      } else {
        for (var index in this.members) {
          var member = this.members[index]
          if (!this.checkedNames.includes(member.name)) {
            member.cost = 0
            member.recharge = 0
          }
        }
      }
    },
    costSum: function (val) {
      if (this.payMode === 'AA') {
        this.setToAA()
      }
    }
  },
  computed: {
    totalRemaining: function () {
      var total = 0
      for (var index in this.members) {
        var member = this.members[index]
        total += member.remaining
      }
      return total
    },
    newTotalRemaining: function () {
      var total = 0
      for (var index in this.members) {
        var member = this.members[index]
        total += member.remaining
        total -= member.cost
        total += member.recharge
      }
      return total
    },
    foundationCost: function () {
      var total = 0
      for (var index in this.members) {
        var member = this.members[index]
        total -= member.cost
      }
      return total
    },
    foundationRecharge: function () {
      var total = 0
      for (var index in this.members) {
        var member = this.members[index]
        total += member.recharge
      }
      return total
    }
  },
  methods: {
    resetCosts: function () {
      if (this.payMode === 'AA') {
        this.setToAA()
      } else {
        for (var index in this.members) {
          var member = this.members[index]
          member.cost = 0
          member.recharge = 0
        }
      }
    },
    setToAA: function () {
      var avgCost = this.costSum / this.checkedNames.length
      for (var index in this.members) {
        var member = this.members[index]
        if (this.checkedNames.includes(member.name)) {
          member.cost = avgCost
        } else {
          member.cost = 0
          member.recharge = 0
        }
      }
    },
    getNewRemaining: function (member) {
      var newRemaining = member.remaining + member.recharge - member.cost
      return newRemaining.toFixed(2)
    },
    submitNewExpense: function () {
      this.submit_error_message = ''

      if (this.eventTime.length === 0) {
        this.submit_error_message = '出错: 无时间'
        return
      }
      if (this.restaurant.length > 0 && this.costSum === 0) {
        this.submit_error_message = '出错: 无支出'
        return
      }
      var balance = this.foundationCost + this.costSum
      if (balance >= 0.02 || balance <= -0.02) {
        this.submit_error_message = '出错: 支出不平衡'
        return
      }

      var expense = {
        restaurant: this.restaurant,
        time: this.eventTime,
        records: []
      }

      for (var index in this.members) {
        var member = this.members[index]
        if (this.checkedNames.includes(member.name)) {
          if (member.cost > 0 || member.recharge > 0) {
            expense.records.push({
              member_id: member.id,
              cost: member.cost,
              recharge: member.recharge
            })
          }
        }
      }

      console.log(expense)

      axios.post('/lunch_foundation/new_report', expense)
      .then((response) => {
        var responseData = response.data
        var err = responseData.error
        if (err) {
          this.submit_error_message = 'Service error: ' + err
        } else {
          this.$router.go(-1)
        }
      }, (error) => {
        this.submit_error_message = 'Service error: ' + error.message
      })
    }
  },
  mounted () {
    axios.get('/lunch_foundation/members')
    .then((response) => {
      for (var index in response.data.result) {
        var member = response.data.result[index]
        member.cost = 0
        member.recharge = 0
        this.members.push(member)
      }
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

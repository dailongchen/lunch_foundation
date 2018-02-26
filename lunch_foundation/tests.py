from django.test import TestCase, RequestFactory

from datetime import datetime, timedelta

from .models import Event, Member, Cost
from .slack import Slack, SlackMessage

# Create your tests here.

class ModelTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        member_1 = Member(name='jacob_1', hidden='0')
        member_1.remaining = 10.0
        member_1.save()
        member_2 = Member(name='jacob_2', hidden='0')
        member_2.remaining = 20.3
        member_2.save()

        for i in range(1, 40):
            eventTime = datetime.now() + timedelta(days=(i-1))
            restaurantName = 'kfc' + str(i)

            Event.submit(restaurantName, eventTime,
                         [{ 'member_id': member_1.id,
                            'cost': 120,
                            'recharge': 100
                         },{ 'member_id': member_2.id,
                            'cost': 210,
                            'recharge': 0
                         }])

    def test_get_last_N_events(self):
        print('last N:', len(Cost.get_costs(Event.get_last_N(3))))

    def test_get_this_week_events(self):
        print('this week:', len(Cost.get_costs(Event.get_this_week())))

    def test_get_this_month_events(self):
        print('this month:', len(Cost.get_costs(Event.get_this_month())))

    def test_get_this_year_events(self):
        print('this year:', len(Cost.get_costs(Event.get_this_year())))

    def test_get_total_remaining(self):
        print('total remaining:', Member.get_total_remaining())

    def test_slack_message(self):
        print('events message:', SlackMessage.events_message(Event.get_last_N(2)))

    # def test_slack_post(self):
    #     message = SlackMessage.events_message(Event.get_last_N(1))
    #     Slack.post(message)

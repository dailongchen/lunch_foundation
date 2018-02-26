from django.db import models

from datetime import datetime, timedelta
import json

# Create your models here.

class Event(models.Model):
    restaurant = models.CharField(max_length=200)
    time = models.DateTimeField('date published')

    def __str__(self):
        return '{0}, {1}'.format(self.restaurant,
                                 self.time)

    @staticmethod
    def get_last_N(n):
        if n == None:
            return Event.objects.order_by('-id')

        return Event.objects.order_by('-id')[:n]

    @staticmethod
    def get_this_week():
        today = datetime.today()
        begin = today - timedelta(days=today.weekday() + 1)
        end = today + timedelta(days=1)
        return Event.objects.filter(time__range=(begin, end)).order_by('-time', '-id')

    @staticmethod
    def get_this_month():
        today = datetime.today()
        begin = datetime(today.year, today.month, 1)
        end = today + timedelta(days=1)
        return Event.objects.filter(time__range=(begin, end)).order_by('-time', '-id')

    @staticmethod
    def get_this_year():
        today = datetime.today()
        begin = datetime(today.year, 1, 1)
        end = today + timedelta(days=1)
        return Event.objects.filter(time__range=(begin, end)).order_by('-time', '-id')

    @staticmethod
    def submit(restaurant, time, records):
        newEvent = Event(restaurant=restaurant, time=time)

        newCosts = []
        for record in records:
            memberId = record['member_id']
            member = Member.objects.get(pk=memberId)
            if member == None:
                return False, "cannot find member with Id: {0}".format(memberId)

            cost = Cost(member=member,
                        cost=record['cost'],
                        recharge=record['recharge'])
            newCosts.append(cost)

        newEvent.save()
        for cost in newCosts:
            cost.event = newEvent
            cost.member.remaining += cost.recharge - cost.cost
            cost.member.save()

            cost.save()

        return True, ""

class Member(models.Model):
    name = models.CharField(max_length=200)
    hidden = models.IntegerField(default=0)
    remaining = models.FloatField(default=0)

    def __str__(self):
        return '{0} (hidden: {1}, remaining: {2})'.format(self.name,
                                                          self.hidden,
                                                          self.remaining)

    def to_json(self):
        return { 'id': self.id,
                 'name': self.name,
                 'hidden': self.hidden,
                 'remaining': float("{:.2f}".format(self.remaining)) }

    @staticmethod
    def get_total_remaining():
        return Member.objects.aggregate(total_remaining=models.Sum('remaining')).get('total_remaining', 0)

    @staticmethod
    def get_members_json():
        members = []
        for member in Member.objects.all():
            members.append(member.to_json())
        return members


class Cost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    cost = models.FloatField(default=0)
    recharge = models.FloatField(default=0)

    class Meta:
        unique_together = ('event', 'member',)

    def __str__(self):
        return '{0}, {1}, {2}, {3}'.format(self.event,
                                           self.member,
                                           self.cost,
                                           self.recharge)

    @staticmethod
    def get_costs(events):
        costs = Cost.objects.filter(event__in=events)
        ret = {}
        for oneCost in costs:
            records = []
            if oneCost.event not in ret:
                ret[oneCost.event] = records
            else:
                records = ret[oneCost.event]

            records.append(oneCost)
        return ret

    @staticmethod
    def get_costs_json(events):
        costs = Cost.get_costs(events)
        ret = []
        for event in events:
            records_json = []
            for cost in costs[event]:
                records_json.append({ 'member': cost.member.to_json(),
                                      'cost': "{:.2f}".format(cost.cost),
                                      'recharge': "{:.2f}".format(cost.recharge), })

            event_json = {
                'restaurant': event.restaurant,
                'time': event.time
            }
            ret.append({
                'event': {
                    'restaurant': event.restaurant,
                    'time': event.time.strftime("%A, %d. %B, %Y")
                },
                'costs': records_json
            })
        return ret

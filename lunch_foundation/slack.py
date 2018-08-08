import json
import random
import ssl
import urllib.request

from .models import Event, Member, Cost

def randomColor():
    r = lambda: random.randint(0,255)
    return('#%02X%02X%02X' % (r(),r(),r()))

class SlackMessage:
    @staticmethod
    def events_message(events):
        attachments = []
        foundationRemaining = Member.get_total_remaining()

        costs = Cost.get_costs(events)
        for event in events:
            totalCost = 0
            totalRecharge = 0

            isRechargeEvent = False
            restaurant = event.restaurant
            if len(restaurant) == 0:
                restaurant = "充值"
                isRechargeEvent = True

            fields = []
            for oneCost in costs[event]:
                totalCost += oneCost.cost
                totalRecharge += oneCost.recharge

                if isRechargeEvent:
                    fields.append({
                        "title": "{0}: +{1:.2f}".format(oneCost.member.name, oneCost.recharge),
                        "value": "余额: {0:.2f}".format(oneCost.member.remaining),
                        "short": True
                    })
                else:
                    rechargeString = ''
                    if oneCost.recharge > 0:
                        rechargeString = "(+{0:.2f}) ".format(oneCost.recharge)

                    fields.append({
                            "title": "{0}: {1:.2f}".format(oneCost.member.name, oneCost.cost),
                            "value": "余额: {0}{1:.2f}".format(rechargeString, oneCost.member.remaining),
                            "short": True
                        })


            eventDescription = []
            if not isRechargeEvent:
                if totalCost > 0:
                    eventDescription.append("消费: {0:.2f}".format(totalCost))
                if totalRecharge > 0:
                    eventDescription.append("充值: {0:.2f}".format(totalRecharge))

            titleText = "*{0} - {1}*\n_ 总账余额: {2:.2f} _\n------------".format(restaurant,
                                                                                 ", ".join(eventDescription),
                                                                                 foundationRemaining)
            attachments.append({ "color": randomColor(),
                                 "text": titleText,
                                 "fields": fields,
                                 "footer": "Lunch Foundation",
                                 "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                                 "ts": int(event.time.timestamp()),
                                 "mrkdwn_in": ["text", "pretext"]
                            })
        return { "attachments": attachments }

class Slack:
    @staticmethod
    def post(message):
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            headers = {
                'Content-Type': 'application/json'
            }
            requestURL = "https://hooks.slack.com/services/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"
            postRequest = urllib.request.Request(requestURL,
                                                 data=json.dumps(message).encode('utf8'),
                                                 headers=headers,
                                                 method='POST')
            postResponse = urllib.request.urlopen(postRequest, context=context)

            print(postResponse.code)
        except urllib.error.HTTPError as e:
            print('  Error: Cannot post message to slack: {0}'.format(e.read()))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
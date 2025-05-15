# notifier/slack_notify.py
import requests

def send_to_slack(msg):
  webhook = "https://hooks.slack.com/services/XXXX/XXXX/XXXX"
  requests.post(webhook, json={"text": msg})

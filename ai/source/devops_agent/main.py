from trigger.detect_failure import check_ci_failure
from fetcher.collector import get_logs, get_commits
from analyzer.analyzer import analyze
from reporter.reporter import generate_report
from notifier.slack_notify import send_to_slack
from memory.memory import save_report

if check_ci_failure():
  logs = get_logs()
  commits = get_commits()
  summary = analyze(logs, commits)
  report = generate_report(summary)
  send_to_slack(report)
  save_report({"summary": summary, "report": report})

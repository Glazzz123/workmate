import json
import argparse
from collections import defaultdict
from tabulate import tabulate
from statistics import median
from datetime import datetime


class LogProcessor:

    def __init__(self):
        self.data = defaultdict(lambda: {'total': 0, 'sum_time': 0, 'times': [], 'logs': []})

    def process_file(self, file_path):

        try:
            with open(file_path, 'r') as f:
                for line in f:
                    log = json.loads(line.strip())
                    if log.get('status') == 200:  # Фильтр по статусу 200
                        self.data[log['url']]['total'] += 1
                        self.data[log['url']]['sum_time'] += log['response_time']
                        self.data[log['url']]['times'].append(log['response_time'])
                        self.data[log['url']]['logs'].append(log)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error processing {file_path}: {e}")


class ReportGenerator:

    @staticmethod
    def generate_average_report(data, date_filter=None):

        filtered_data = defaultdict(lambda: {'total': 0, 'sum_time': 0, 'times': []})
        for url, stats in data.items():
            for log in stats['logs']:
                log_date = datetime.fromisoformat(log['@timestamp'].replace('Z', '+00:00'))
                if not date_filter or log_date.date() == date_filter:
                    filtered_data[url]['total'] += 1
                    filtered_data[url]['sum_time'] += log['response_time']
                    filtered_data[url]['times'].append(log['response_time'])

        report_data = []
        for url, stats in filtered_data.items():
            avg_time = stats['sum_time'] / stats['total'] if stats['total'] > 0 else 0
            med_time = median(stats['times']) if stats['times'] else 0
            report_data.append([url, stats['total'], round(avg_time, 3), round(med_time, 3)])

        report = tabulate(report_data, headers=['handler', 'total', 'avg_response_time', 'median_response_time'],
                          tablefmt='grid')
        json_data = {
            url: {
                'total': stats['total'],
                'avg_response_time': round(stats['sum_time'] / stats['total'], 3) if stats['total'] > 0 else 0,
                'median_response_time': round(median(stats['times']), 3) if stats['times'] else 0
            }
            for url, stats in filtered_data.items()
        }
        return report, json_data

    @staticmethod
    def generate_user_agent_report(data, date_filter=None):
        user_agents = defaultdict(int)
        for url, stats in data.items():
            for log in stats['logs']:
                log_date = datetime.fromisoformat(log['@timestamp'].replace('Z', '+00:00'))
                if not date_filter or log_date.date() == date_filter:
                    user_agent = log.get('http_user_agent', 'Unknown')
                    user_agents[user_agent] += 1

        report_data = [[ua, count] for ua, count in user_agents.items()]
        report = tabulate(report_data, headers=['user_agent', 'count'], tablefmt='grid')
        json_data = {ua: count for ua, count in user_agents.items()}
        return report, json_data


def main():
    parser = argparse.ArgumentParser(description='Generate customizable reports from log files.')
    parser.add_argument('--file', nargs='+', help='List of log files to process', required=True)
    parser.add_argument('--report', choices=['average', 'user_agent'], default='average',
                        help='Type of report to generate')
    parser.add_argument('--date', type=str, help='Filter logs by date (YYYY-MM-DD), e.g., 2025-06-22')
    args = parser.parse_args()

    processor = LogProcessor()
    for file_path in args.file:
        processor.process_file(file_path)

    date_filter = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else None

    if args.report == 'average':
        report, json_data = ReportGenerator.generate_average_report(processor.data, date_filter)
    elif args.report == 'user_agent':
        report, json_data = ReportGenerator.generate_user_agent_report(processor.data, date_filter)
    else:
        report = "No valid report type specified."
        json_data = {}

    print(report)
    with open('report.json', 'w') as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    main()

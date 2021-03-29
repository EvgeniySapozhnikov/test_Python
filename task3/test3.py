import datetime
import re
import csv
import sys


def update_statistic(args, statistic, log_line):
    pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).+ wanna (\w+.\w+) (\d+)l .(\w+)'
    line_elements = re.match(pattern, log_line)
    line_time = datetime.datetime.strptime(line_elements[1], '%Y-%m-%dT%H:%M:%S')
    if args['st_time'] <= line_time <= args['stp_time']:
        if line_elements[2] == 'top up':
            statistic['Количество вливаний'] += 1
            if line_elements[4] == 'успех':
                statistic['Налитый объем'] += int(line_elements[3])
                args['current_v'] += int(line_elements[3])
            elif line_elements[4] == 'фейл':
                statistic['Неналитый объем'] += int(line_elements[3])
                args['top_up_err'] += 1
        elif line_elements[2] == 'scoop':
            statistic['Количество заборов'] += 1
            if line_elements[4] == 'успех':
                statistic['Забранный объем'] += int(line_elements[3])
                args['current_v'] -= int(line_elements[3])
            elif line_elements[4] == 'фейл':
                statistic['Незабранный объем'] += int(line_elements[3])
                args['scoop_err'] += 1
        statistic['Конечный объем'] = args['current_v']
    else:
        if line_elements[2] == 'top up' and line_elements[4] == 'успех':
            args['current_v'] += int(line_elements[3])
        elif line_elements[2] == 'scoop' and line_elements[4] == 'успех':
            args['current_v'] -= int(line_elements[3])
    return


def write_results(args, statistic):
    if statistic['Количество вливаний'] + statistic['Количество заборов'] > 0:
        statistic['Период'] = str(args['stp_time'] - args['st_time'])
        statistic['Начальный объем'] = statistic['Конечный объем'] - statistic["Налитый объем"] + statistic["Забранный объем"]
        statistic['Процент неудачных вливаний'] = round((args['top_up_err'] / statistic['Количество вливаний']) * 100)
        statistic['Процент неудачных заборов'] = round((args['scoop_err'] / statistic['Количество заборов']) * 100)

        with open('results.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for res_line in [list(statistic.keys()), list(statistic.values())]:
                writer.writerow(res_line)
    return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        args = {'top_up_err': 0, 'scoop_err': 0}
        statistic = {"Период": 0, "Количество вливаний": 0, "Процент неудачных вливаний": 0, "Налитый объем": 0,
                     "Неналитый объем": 0, "Количество заборов": 0, "Процент неудачных заборов": 0,
                     "Забранный объем": 0, "Незабранный объем": 0, "Начальный объем": 0, "Конечный объем": 0}
        try:
            args['log_path'] = re.match(r'(.+log)', sys.argv[1])[1]
            args['st_time'] = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%S')
            args['stp_time'] = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%dT%H:%M:%S')
            if args['st_time'] >= args['stp_time']:
                raise NameError('Начальное время больше конечного')

            with open(args['log_path'], 'r', encoding='utf-8') as f:
                f.readline()
                f.readline()
                args['current_v'] = int(re.match(r'(\d+)', f.readline()).group(1))

                for line in f:
                    update_statistic(args, statistic, line)
                write_results(args, statistic)
        except:
            print('введите атрибуты в формате: python script_name.py log_path start_time stop_time')
    else:
        print('введите атрибуты в формате: python script_name.py log_path start_time stop_time')

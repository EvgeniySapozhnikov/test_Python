import datetime
import re
import csv
import sys


class BarrelStatistic:
    """Данный класс обеспечивает хранение и обновление статистики, а также записывает разультаты в csv"""
    def __init__(self, current_v, st_time, stp_time):
        self.st_v = 0
        self.stp_v = 0
        self.current_v = current_v
        self.st_time = st_time
        self.stp_time = stp_time
        self.statistic = {'top up': {'number': 0, 'err_number': 0, 'err_percent': 0, 'success_v': 0, 'err_v': 0},
                          'scoop': {'number': 0, 'err_number': 0, 'err_percent': 0, 'success_v': 0, 'err_v': 0},
                          'st_v': 0,
                          'stp_v': 0}

    def update_statistic(self, log_line):
        pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).+ wanna (\w+.\w+) (\d+)l .(\w+)'
        line_elements = re.match(pattern, log_line)
        line_time = datetime.datetime.strptime(line_elements[1], '%Y-%m-%dT%H:%M:%S')
        if self.st_time <= line_time <= stp_time:
            if line_elements[2] == 'top up':
                self.statistic['top up']['number'] += 1
                if line_elements[4] == 'успех':
                    self.statistic['top up']['success_v'] += int(line_elements[3])
                    self.current_v += int(line_elements[3])
                elif line_elements[4] == 'фейл':
                    self.statistic['top up']['err_v'] += int(line_elements[3])
                    self.statistic['top up']['err_number'] += 1
            elif line_elements[2] == 'scoop':
                self.statistic['scoop']['number'] += 1
                if line_elements[4] == 'успех':
                    self.statistic['scoop']['success_v'] += int(line_elements[3])
                    self.current_v -= int(line_elements[3])
                elif line_elements[4] == 'фейл':
                    self.statistic['scoop']['err_v'] += int(line_elements[3])
                    self.statistic['scoop']['err_number'] += 1
            self.stp_v = self.current_v
        else:
            if line_elements[2] == 'top up' and line_elements[4] == 'успех':
                self.current_v += int(line_elements[3])
            elif line_elements[2] == 'scoop' and line_elements[4] == 'успех':
                self.current_v -= int(line_elements[3])
        return

    def write_results(self):
        if self.statistic['scoop']['number'] + self.statistic['top up']['number'] > 0:
            self.st_v = self.stp_v - self.statistic["top up"]["success_v"] + self.statistic["scoop"]["success_v"]
            self.statistic['top up']['err_percent'] = round((self.statistic['top up']['err_number'] /
                                                             self.statistic['top up']['number']) * 100)
            self.statistic['scoop']['err_percent'] = round((self.statistic['scoop']['err_number'] /
                                                            self.statistic['scoop']['number']) * 100)
            results = [["Период", "Количество вливаний", "Процент неудачных вливаний", "Налитый объем",
                        "Неналитый объем", "Количество заборов", "Процент неудачных заборов", "Забранный объем",
                        "Незабранный объем", "Начальный объем", "Конечный объем"],
                       [str(self.stp_time - self.st_time),
                        self.statistic['top up']['number'], self.statistic['top up']['err_percent'],
                        self.statistic['top up']['success_v'], self.statistic['top up']['err_v'],
                        self.statistic['scoop']['number'], self.statistic['scoop']['err_percent'],
                        self.statistic['scoop']['success_v'], self.statistic['scoop']['err_v'],
                        self.st_v, self.stp_v]]

            with open('results.csv', 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                for res_line in results:
                    writer.writerow(res_line)
        return

    def __repr__(self):
        current_state = f'st_v={self.stp_v - self.statistic["top up"]["success_v"] + self.statistic["scoop"]["success_v"]} ' + \
                        f'stp_v={self.stp_v} ' + \
                        f'st_time={self.st_time}, stp_time={self.stp_time} ' + \
                        f'{self.statistic}'
        return current_state


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            log_path = re.match(r'(.+log)', sys.argv[1])[1]
            st_time = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%S')
            stp_time = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%dT%H:%M:%S')
            if st_time >= stp_time:
                raise NameError('Начальное время больше конечного')

            with open(log_path, 'r', encoding='UTF-8') as f:
                f.readline()
                f.readline()
                current_v = int(re.match(r'(\d+)', f.readline()).group(1))

                stat = BarrelStatistic(current_v=current_v, st_time=st_time, stp_time=stp_time)

                for line in f:
                    stat.update_statistic(line)
                stat.write_results()
        except:
            print('введите атрибуты в формате: python script_name.py log_path start_time stop_time')
    else:
        print('введите атрибуты в формате: python script_name.py log_path start_time stop_time')

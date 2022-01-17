import datetime
import json
import re
import uuid
import requests


def gen_file(_anime_msg_list):
    today = datetime.datetime.today()
    file_name = 'anime_cal_'+str(today.year) + str(today.month).zfill(2)+'.ics'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('BEGIN:VCALENDAR\n')
        f.write('VERSION:2.0\n')
        f.write('PRODID:-//JH-L//JH-L Calendar//\n')

        anime_set = set()

        for each in _anime_msg_list:

            if each['name'] in anime_set:
                continue
            anime_set.add(each['name'])

            try:
                each['startDate'].replace('-', '').replace(':', '')[:-5]
            except KeyError:
                print(f"无日期的番剧: {each['name']}")
                continue

            f.write('BEGIN:VEVENT\n')
            f.write(f"SUMMARY:{each['name']}\n")

            t_str = each['startDate'].replace('-', '').replace(':', '')[:-5]

            t = datetime.datetime.strptime(t_str, '%Y%m%dT%H%M%S')
            f.write(f"DTSTART;TZID=\"UTC+08:00\";VALUE=DATE-TIME:{t.strftime('%Y%m%dT%H%M%S')}\n")

            t += datetime.timedelta(minutes=25)
            f.write(f"DTEND;TZID=\"UTC+08:00\";VALUE=DATE-TIME:{t.strftime('%Y%m%dT%H%M%S')}\n")

            t += datetime.timedelta(days=7 * 4 * 3)
            f.write(f"RRULE:FREQ=WEEKLY;UNTIL={t.strftime('%Y%m%dT%H%M%S')}\n")
            f.write(f"UID:{uuid.uuid1()}\n")

            f.write('END:VEVENT\n')

        f.write('END:VCALENDAR')


def get_anime_msg():
    # 绕开操作系统挂的梯子
    proxies = {'http': None, 'https': None}

    print("开始爬取数据...")

    today = datetime.datetime.today()
    url = 'https://acgsecrets.hk/bangumi/'+str(today.year)+str(today.month).zfill(2)+'/'
    r = requests.get(url, proxies=proxies)

    print("爬取数据完成")

    r.encoding = 'utf-8'

    regex = r'"itemListElement":\[.+?}\]}'
    raw_msg = re.findall(regex, r.text)[0][18:-1]

    _anime_msg_list = json.loads(raw_msg)

    print(json.dumps(_anime_msg_list, sort_keys=True, indent=4, separators=(',', ': ')))

    return _anime_msg_list


if __name__ == '__main__':
    print('Start Running!')

    anime_msg_list = get_anime_msg()

    gen_file(anime_msg_list)

    input('End Running!')

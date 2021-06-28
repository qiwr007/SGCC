# coding:utf-8
import csv
import codecs
import numpy as np
from scipy.stats import norm, gamma, invgamma
import random
import datetime

if __name__ == '__main__':
    data = ('设备型号', '安装时间', '厂家', '损坏时间', '设计寿命', '温度', '湿度', '安装地点', '间隔', '运维班', '损坏性质')

    f = codecs.open('fake_data_with_string_label.csv', 'w', 'gbk')
    writer = csv.writer(f)
    writer.writerow(data)

    # generate our model data
    equipments = ['显示屏', 'CPU板件', '电源DC220']  # how many equipments we have
    manufacturers = ['许继电气', '上海惠安', '深圳南瑞', '南瑞科技', '国电南自', '南瑞继保']  # the manufacturers

    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2020, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    weathers = ['晴', '阴', '雷阵雨', '冰雹', '小雨', '大雨']

    maintenances = ['维修班1', '维修班2', '维修班3', '维修班4']

    states = ['保护装置故障', '开关设备故障', '电流互感器二次回路故障', '电压互感器二次回路故障', '继电器触点故障', '直流接地', '老化']

    for i in range(10000):
        # 1. the name of equipment
        equipment = random.choice(equipments)

        # 2. the date to set up the equipment
        random_number_of_days = random.randrange(days_between_dates)  # uniform distribution
        set_date = start_date + datetime.timedelta(days=random_number_of_days)  # uni-distri to get set date

        # 3. who produce the equipment
        manufacturer = random.choice(manufacturers)

        # 5. the planned longitude
        planned_life = random.randint(3, 15)

        # 4. the actual broken date
        planned_broken_date = set_date + datetime.timedelta(days=planned_life*365)
        a = 4.07
        life_difference = datetime.timedelta(days=invgamma.rvs(a)*365*-1)  # the difference between given life and actual life
        broken_date = planned_broken_date + life_difference

        # 6. the weather when it was broken
        weather = random.choice(weathers)

        # 7. its location
        location = 'somewhere'

        # 8. maintenance people
        maintenance = random.choice(maintenances)

        # 9. the present state of the equipment
        if broken_date > datetime.date(2021, 6, 7):
            state = 0  # if the estimated broken date exceeds today, the equipment is normal
        else:
            state = random.choice(states)  # otherwise, it has some unusual state

        writer.writerow((equipment, set_date, manufacturer, broken_date, planned_life, weather, location, maintenance, state))
    f.close()

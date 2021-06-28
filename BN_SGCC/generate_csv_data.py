# coding:utf-8
import csv
import codecs
import numpy as np
from scipy.stats import norm, gamma, invgamma
import random
import datetime

if __name__ == '__main__':
    data = ('设备型号', '安装时间', '厂家', '损坏时间', '设计寿命', '损坏时的天气', '安装地点', '运维班', '损坏性质')

    f = codecs.open('fake_data.csv', 'w', 'gbk')
    writer = csv.writer(f)
    writer.writerow(data)

    # generate our model data
    equipments = [1, 2, 3]
    # ['显示屏', 'CPU板件', '电源DC220']  # how many equipments we have
    manufacturers = [1, 2, 3, 4, 5, 6]
    # ['许继电气', '上海惠安', '深圳南瑞', '南瑞科技', '国电南自', '南瑞继保']  # the manufacturers

    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date(2020, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    weathers = [1, 2, 3, 4, 5, 6]  # ['晴', '阴', '雷阵雨', '冰雹', '小雨', '大雨']

    maintenances = [1, 2, 3, 4]

    states = [1, 2, 3, 4, 5, 6, 7]

    # some counts
    sampleSize = 10000
    countNormal = 0
    countBrokenBeforePlan = 0
    countBrokenAfterPlan = 0

    for i in range(sampleSize):
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
        dist_sample = gamma.rvs(a, loc=3, scale=0.7) - 4.5  # rvs(a, loc=0, scale=1, size=1, random_state=None)
        if dist_sample > 0:
            countBrokenBeforePlan += 1
        else:
            countBrokenAfterPlan += 1
        life_difference = datetime.timedelta(days=dist_sample*365)  # the difference between given life and actual life
        broken_date = planned_broken_date + life_difference


        # 6. the weather when it was broken
        weather = random.choice(weathers)

        # 7. its location
        location = 0

        # 8. maintenance people
        maintenance = random.choice(maintenances)

        # 9. the present state of the equipment
        if broken_date > datetime.date(2021, 6, 7):
            state = 0  # if the estimated broken date exceeds today, the equipment is normal
            countNormal += 1
        else:
            state = random.choice(states)  # otherwise, it has some unusual state

        writer.writerow((equipment, set_date, manufacturer, broken_date, planned_life, weather, location, maintenance, state))
    f.close()

    normalRate = countNormal/sampleSize
    print('normal rate is: ', normalRate)
    brokenRateBefore = countBrokenBeforePlan / sampleSize
    brokenRateAfter = countBrokenAfterPlan / sampleSize
    print('broken before planned rate is: ', brokenRateBefore)
    print('broken after planned rate is: ', brokenRateAfter)
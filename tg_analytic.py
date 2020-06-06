#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import pandas as pd

users_type = {
    1: 'пользователь',
    2: 'пользователя',
    3: 'пользователя',
    4: 'пользователя'
}
day_type = {
    1: 'день',
    2: 'дня',
    3: 'дня',
    4: 'дня'
}

# remove txt file
def remove(user_id):
    path = os.getcwd() + '/%s.txt' % user_id
    os.remove(path)


# write data to csv
def statistics(user_id, command):
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    with open('data.csv', 'a', newline="") as fil:
        wr = csv.writer(fil, delimiter=';')
        wr.writerow([data, user_id, command])


# make report
def analysis(bid, user_id):
    season = int(bid[1])
    df = pd.read_csv('data.csv', delimiter=';', encoding='utf8')
    number_of_users = len(df['id'].unique())
    number_of_days = len(df['data'].unique())

    message_to_user = 'Статистика использования бота за %s %s: \n' % (season, day_type.get(season, 'дней'))
    message_to_user += 'Всего статистика собрана за %s %s \n' % (number_of_days, day_type.get(season, 'дней'))
    if season > number_of_days:
        season = number_of_days
        message_to_user += 'Указанное вами количество дней больше,чем имеется\n' \
                           'Будет выведена статистика за максимальное возможное время\n'

    df_user = df.groupby(['data', 'id']).count().reset_index().groupby('data').count().reset_index()
    list_of_dates_in_df_user = list(df_user['data'])
    list_of_number_of_user_in_df_user = list(df_user['id'])
    list_of_dates_in_df_user = list_of_dates_in_df_user[-season:]
    list_of_number_of_user_in_df_user = list_of_number_of_user_in_df_user[-season:]
    df_command = df.groupby(['data', 'command']).count().reset_index()
    unique_commands = df['command'].unique()
    commands_in_each_day = []
    list_of_dates_in_df_command = list(df_command['data'])
    list_of_number_of_user_in_df_command = list(df_command['id'])
    list_of_name_of_command_in_df_command = list(df_command['command'])
    commands_in_this_day = dict()
    for i in range(len(list_of_dates_in_df_command)):
        commands_in_this_day[list_of_name_of_command_in_df_command[i]] = list_of_number_of_user_in_df_command[i]
        if i + 1 >= len(list_of_dates_in_df_command) or list_of_dates_in_df_command[i] != list_of_dates_in_df_command[
            i + 1]:
            commands_in_each_day.append(commands_in_this_day)
            commands_in_this_day = dict()
    commands_in_each_day = commands_in_each_day[-season:]

    if 'пользователи' in bid:
        message_to_user += 'За всё время бота использовало ' + '%s' % number_of_users \
                           + ' %s ' % users_type.get(number_of_users, 'пользователей') + '\n' \
                                                                                         'Пользователей за последние %s %s: \n' % (
                               season, day_type.get(season, 'дней'))
        for days, number, comm_day in zip(list_of_dates_in_df_user, list_of_number_of_user_in_df_user,
                                          commands_in_each_day):
            message_to_user += 'Дата:%s Количество:%d Из них новых:%s\n' % (days, number, comm_day.get('/start', 0))
    if 'команды' in bid:
        message_to_user += 'Статистика команд за последние %s %s: \n' % (season, day_type.get(season, 'дней'))
        for days, commands in zip(list_of_dates_in_df_user, commands_in_each_day):
            message_to_user += 'Дата:%s\n' % days
            for i in unique_commands:
                if i in commands:
                    message_to_user += '%s - %s раз\n' % (i, commands.get(i))
                else:
                    message_to_user += '%s - 0 раз\n' % i

    if 'txt' in bid or 'тхт' in bid:
        with open('%s.txt' % user_id, 'w', encoding='UTF-8') as fil:
            fil.write(message_to_user)
            fil.close()
    else:
        return message_to_user

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import collections
pd.set_option("display.min_rows", 200)
pd.set_option("display.max_rows", 999)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('stats-310310-dad4c31922c5.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Stats')
sheet_instance = sheet.get_worksheet(5)
cur_list = sheet_instance.get_all_records()

teams = []
players_list = []
for player in cur_list:
    if player.get('Team') not in teams:
        teams.append(player.get('Team'))
    if player.get('Score') != '' and player.get('Price') != 0:
        player['Score'] = str(player.get('Score')).replace(',','.')
        player['Price'] = str(player.get('Price')).replace(',', '.')
    players_list.append([player.get('Team'), player.get('Player'), [player.get('Role'), float(player.get('Score')), float(player.get('Price'))]])
    del player['Total Count']
    del player['Wins']
    del player['Losses']
    del player['Winrate']
    del player['As Radiant']
    del player['As Dire']
    del player['Kills']
    del player['Deaths']
    del player['Assists']
    del player['KDA']
    del player['Avg. KAL']
    del player['GPM']
    del player['XPM']
    del player['Last Hits']
    del player['Denies']
    del player['LVL']
    del player['HD']
    del player['TD']
    del player['HH']
    del player['GS']
    del player['Wards']
    del player['Camps']
    del player['']


for team in teams:
    temp = {}
    for player in players_list:
        if player[0] == team:
            temp[str(player[1])] = player[2]
    locals()[str(team)] = temp


def checking_cores (*names):
    x = 0
    if len(check_cores) == 0: return 1
    for name in names:
        if check_cores.count(name) == 1:
            x = x+1
    if x == len(check_cores):
        return 1
    else: return 0


def checking_sups (*names):
    x = 0
    if len(check_sups) == 0: return 1
    for name in names:
        if check_sups.count(name) == 1:
            x = x+1
    if x == len(check_sups):
        return 1
    else: return 0


def ex_sups (*names):
    x = 0
    if len(exclude_sups) == 0: return 1
    for name in names:
        if exclude_sups.count(name) == 1:
            x = x+1
    if x > 0:
        return 0
    else: return 1


def ex_cores (*names):
    x = 0
    if len(exclude_cores) == 0: return 1
    for name in names:
        if exclude_cores.count(name) == 1:
            x = x+1
    if x > 0:
        return 0
    else: return 1

while True:
    playing = []
    for x in range(len(teams)):
        print(f"{x+1}: {teams[x]}\t")
    who = input('Кто сегодня выиграет? Если нужна общая статистика,\nвведите all: ')
    if who == "all":
        playing = teams
    else:
        who = who.split()
        for f in range(len(who)):
            playing.append(teams[int(who[f])-1])
    del who
    number = int(input('Сколько комбинаций нужно?: '))

    sup_nicks = []
    sup_price = []
    sup_pts = []
    core_nicks = []
    core_price = []
    core_pts = []
    setup = []
    setup1 = []
    setup_all = []
    setup_all1 = []

    check_cores = []
    check_sups = []
    exclude_cores = []
    exclude_sups = ['tOfu']


    for team in playing:
        nicks = eval(team).keys()
        for nick in nicks:
            if eval(team).get(nick)[0] == 'C':
                core_nicks.append(nick)
                core_pts.append(eval(team).get(nick)[1])
                core_price.append(eval(team).get(nick)[2])
            elif eval(team).get(nick)[0] == 'S':
                sup_nicks.append(nick)
                sup_pts.append(eval(team).get(nick)[1])
                sup_price.append(eval(team).get(nick)[2])

    for i in range(len(sup_nicks)):
        for j in range(i+1, len(sup_nicks)):
            for k in range(len(core_nicks)):
                for l in range(k+1, len(core_nicks)):
                    for m in range(l+1, len(core_nicks)):
                        score = sup_pts[i] + sup_pts[j] + core_pts[k] + core_pts[l] + core_pts[m]
                        price = sup_price[i] + sup_price[j] + core_price[k] + core_price[l] + core_price[m]
                        if price <= 50:
                            setup1.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')',
                                           sup_nicks[j] + ' (' + str(sup_pts[j]) + ')',
                                           core_nicks[k] + ' (' + str(core_pts[k]) + ')',
                                           core_nicks[l] + ' (' + str(core_pts[l]) + ')',
                                           core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
                            if (checking_cores(core_nicks[k], core_nicks[l], core_nicks[m]) and (checking_sups(sup_nicks[i], sup_nicks[j]))): # and (core_nicks[l] or core_nicks[m]) in check_cores
                                if (ex_sups(sup_nicks[i], sup_nicks[j]) and ex_cores(core_nicks[k], core_nicks[l], core_nicks[m])): #
                                    setup.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')', sup_nicks[j]+ ' (' + str(sup_pts[j]) + ')', core_nicks[k] + ' (' + str(core_pts[k]) + ')', core_nicks[l] + ' (' + str(core_pts[l]) + ')', core_nicks[m] + ' (' + str(core_pts[m]) + ')'])

    sup_nicks = []
    sup_price = []
    sup_pts = []
    core_nicks = []
    core_price = []
    core_pts = []

    for team in teams:
        nicks = eval(team).keys()
        for nick in nicks:
            if eval(team).get(nick)[0] == 'C':
                core_nicks.append(nick)
                core_pts.append(eval(team).get(nick)[1])
                core_price.append(eval(team).get(nick)[2])
            elif eval(team).get(nick)[0] == 'S':
                sup_nicks.append(nick)
                sup_pts.append(eval(team).get(nick)[1])
                sup_price.append(eval(team).get(nick)[2])

    for i in range(len(sup_nicks)):
        for j in range(i+1, len(sup_nicks)):
            for k in range(len(core_nicks)):
                for l in range(k+1, len(core_nicks)):
                    for m in range(l+1, len(core_nicks)):
                        score = sup_pts[i] + sup_pts[j] + core_pts[k] + core_pts[l] + core_pts[m]
                        price = sup_price[i] + sup_price[j] + core_price[k] + core_price[l] + core_price[m]
                        if price <= 50:
                            # setup_all.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')',
                            #                sup_nicks[j] + ' (' + str(sup_pts[j]) + ')',
                            #                core_nicks[k] + ' (' + str(core_pts[k]) + ')',
                            #                core_nicks[l] + ' (' + str(core_pts[l]) + ')',
                            #                core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
                            # if (checking_cores(core_nicks[k], core_nicks[l], core_nicks[m]) and (checking_sups(sup_nicks[i], sup_nicks[j]))): # and (core_nicks[l] or core_nicks[m]) in check_cores
                            #     if (ex_sups(sup_nicks[i], sup_nicks[j]) and ex_cores(core_nicks[k], core_nicks[l], core_nicks[m])): #
                                    setup_all1.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')', sup_nicks[j]+ ' (' + str(sup_pts[j]) + ')', core_nicks[k] + ' (' + str(core_pts[k]) + ')', core_nicks[l] + ' (' + str(core_pts[l]) + ')', core_nicks[m] + ' (' + str(core_pts[m]) + ')'])

    setup_all1.sort(key=lambda i: i[0], reverse=True)
    setup.sort(key=lambda i: i[0], reverse=True)
    setup1.sort(key=lambda i: i[0], reverse=True)
    top_score = setup_all1[0][0]
    setup = setup[0:number]
    setup1 = setup1[0:number]
    for i in range(len(setup)):
        setup[i].insert(0, setup_all1.index(setup[i]))
        setup[i].insert(2, setup[i][1]-top_score)

    df = pd.DataFrame(setup, columns=['Orig Pos', 'Score', 'Diff', 'Price', 'Sup1', 'Sup2', 'Core1', 'Core2', 'Core3'])
    pd.set_option('display.expand_frame_repr', False)
    df = df.set_index('Orig Pos')
    print(df)
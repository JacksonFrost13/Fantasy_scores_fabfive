import gspread, sys
from oauth2client.service_account import ServiceAccountCredentials
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from mydesign import Ui_MainWindow
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('stats-310310-dad4c31922c5.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Stats') #EU 3-4, CN 5-6, CIS 7-8

Region = 0
check_cores = []
check_sups = []
exclude_cores = []
exclude_sups = []
# winlist_orig = []
# loselist_orig = []
# players_list_win = []
# players_list_lose = []
player_in = []
player_out = []

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.RegionChoose()
        self.ui.region.currentIndexChanged.connect(self.RegionChoose)
        self.ui.final_2.clicked.connect(self.Calculate)
        self.ui.cores_in.selectionModel().selectionChanged.connect(self.SearchPlayerIn)
        self.ui.cores_out.selectionModel().selectionChanged.connect(self.SearchPlayerOut)
        self.ui.sups_in.selectionModel().selectionChanged.connect(self.SearchPlayerIn)
        self.ui.sups_out.selectionModel().selectionChanged.connect(self.SearchPlayerOut)
        self.ui.clear_sel_sups_in.clicked.connect(self.ui.sups_in.clearSelection)
        self.ui.clear_sel_cores_in.clicked.connect(self.ui.cores_in.clearSelection)
        self.ui.clear_sel_sups_out.clicked.connect(self.ui.sups_out.clearSelection)
        self.ui.clear_sel_cores_out.clicked.connect(self.ui.cores_out.clearSelection)


    def RegionChoose(self):
        Region = int(self.ui.region.currentIndex()+1)
        self.ui.score_matrix.clear()
        winlist_orig = sheet.get_worksheet(Region * 2 + 1).get_all_records()
        loselist_orig = sheet.get_worksheet(Region * 2 + 2).get_all_records()
        players_list_win = []
        players_list_lose = []
        deleting(winlist_orig, players_list_win)
        deleting(loselist_orig, players_list_lose)

        self.ui.cores_in.clear()
        self.ui.cores_out.clear()
        self.ui.sups_in.clear()
        self.ui.sups_out.clear()

        for team in teams:
            temp = {}
            for player in players_list_win:
                if player[0] == team:
                    temp[str(player[1])] = player[2]
            globals()[str(team + '_win')] = temp
            for nick in temp.keys():
                if temp.get(nick)[0] == 'C':
                    self.ui.cores_in.addItem(nick)
                    self.ui.cores_out.addItem(nick)
                elif temp.get(nick)[0] == 'S':
                    self.ui.sups_in.addItem(nick)
                    self.ui.sups_out.addItem(nick)

        for team in teams:
            temp = {}
            for player in players_list_lose:
                if player[0] == team:
                    temp[str(player[1])] = player[2]
            globals()[str(team + '_lose')] = temp

        self.ui.score_matrix.setColumnCount(len(teams))
        self.ui.score_matrix.setRowCount(len(teams))
        self.ui.score_matrix.setHorizontalHeaderLabels(teams)
        self.ui.score_matrix.setVerticalHeaderLabels(teams)
        self.ui.score_matrix.horizontalHeader().setFixedHeight(25)
        self.ui.score_matrix.verticalHeader().setFixedWidth(75)
        for it in range(len(teams)):
            self.ui.score_matrix.setColumnWidth(it, 75)
            self.ui.score_matrix.setRowHeight(it, 35)
        #self.ui.score_matrix.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        for row in range(len(teams)):
            for col in range(len(teams)):
                self.ui.score_matrix.setItem(row, col, QTableWidgetItem())
                item = self.ui.score_matrix.item(row, col)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QtGui.QFont('Segoe UI', 12))
        for row in range(len(teams)):
            for col in range(row+1):
                item = self.ui.score_matrix.item(row, col)
                item.setBackground(QtGui.QColor(150, 150, 150))
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)


    def SearchPlayerIn(self):
        global player_in
        global player_out
        player_in = []
        for player1 in self.ui.cores_in.selectedItems():
            player_in.append(player1)
        for player1 in self.ui.sups_in.selectedItems():
            player_in.append(player1)
        for index in range(self.ui.cores_out.count()):
            row = self.ui.cores_out.item(index)
            row.setFlags(row.flags() | Qt.ItemIsEnabled)
        for index in range(self.ui.sups_out.count()):
            row = self.ui.sups_out.item(index)
            row.setFlags(row.flags() | Qt.ItemIsEnabled)
        for index in self.ui.cores_in.selectedIndexes():
            row = index.row()
            item = self.ui.cores_out.item(row)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        for index in self.ui.sups_in.selectedIndexes():
            row = index.row()
            item = self.ui.sups_out.item(row)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        column = range(3, 8)
        flag_in = 0
        flag_out = 0
        for row in range(self.ui.output_table.rowCount()):
            for col in column:
                for one in player_in:
                    if one.text() in self.ui.output_table.item(row, col).text():
                        flag_in += 1
                for two in player_out:
                    if two.text() in self.ui.output_table.item(row, col).text():
                        flag_out += 1
            if flag_in == len(player_in) and flag_out == 0:
                self.ui.output_table.showRow(row)
                flag_in = 0
            else:
                self.ui.output_table.hideRow(row)
                flag_in = 0
                flag_out = 0

    def SearchPlayerOut(self):
        global player_in
        global player_out
        player_out = []
        for player1 in self.ui.cores_out.selectedItems():
            player_out.append(player1)
        for player1 in self.ui.sups_out.selectedItems():
            player_out.append(player1)
        for index in range(self.ui.cores_in.count()):
            row = self.ui.cores_in.item(index)
            row.setFlags(row.flags() | Qt.ItemIsEnabled)
        for index in range(self.ui.sups_in.count()):
            row = self.ui.sups_in.item(index)
            row.setFlags(row.flags() | Qt.ItemIsEnabled)
        for index in self.ui.cores_out.selectedIndexes():
            row = index.row()
            item = self.ui.cores_in.item(row)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        for index in self.ui.sups_out.selectedIndexes():
            row = index.row()
            item = self.ui.sups_in.item(row)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        column = range(3, 8)
        flag_in = 0
        flag_out = 0
        for row in range(self.ui.output_table.rowCount()):
            for col in column:
                for two in player_out:
                    if two.text() in self.ui.output_table.item(row, col).text():
                        flag_out += 1
                for one in player_in:
                    if one.text() in self.ui.output_table.item(row, col).text():
                        flag_in += 1
            if flag_out > 0 or flag_in != len(player_in):
                self.ui.output_table.hideRow(row)
                flag_out = 0
                flag_in = 0
            else:
                self.ui.output_table.showRow(row)
                flag_out = 0
                flag_in = 0

    def Calculate(self):
        global player_in
        global player_out
        player_in = []
        player_out = []
        self.ui.sups_in.clearSelection
        self.ui.cores_in.clearSelection
        self.ui.sups_out.clearSelection
        self.ui.cores_out.clearSelection
        self.ui.output_table.clear()

        global playing
        playing = []
        global teams_with_score
        teams_with_score = []

        for team in teams:
            teams_with_score.append([team, 0, 0])
        num_rows, num_cols = self.ui.score_matrix.rowCount(), self.ui.score_matrix.columnCount()
        for i in range(0, num_rows):
            for j in range(i+1, num_cols):
                scorex = self.ui.score_matrix.item(i, j)
                #self.ui.label_10.setText(scorex)
                if (scorex and scorex.text()):
                    team1 = self.ui.score_matrix.horizontalHeaderItem(i).text()
                    team2 = self.ui.score_matrix.verticalHeaderItem(j).text()
                    if team1 not in playing:
                        playing.append(team1)
                    if team2 not in playing:
                        playing.append(team2)
                    scorex = scorex.text()
                    scorex = scorex.split('-')
                    for teamz in teams_with_score:
                        if teamz[0] == team1:
                            teamz[1] += int(scorex[0])
                            teamz[2] += 2 - int(scorex[0])
                        elif teamz[0] == team2:
                            teamz[1] += int(scorex[1])
                            teamz[2] += 2 - int(scorex[1])

        team_multis = {teamx[0]: teamx[1:] for teamx in teams_with_score}
        for team in playing:
            temporary = globals()[str(team+'_win')]
            globals()[str(team)] = temporary.copy()
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

        for team in playing:
            nicks = eval(team).keys()
            for nick in nicks:
                if eval(team).get(nick)[0] == 'C':
                    core_nicks.append(nick)
                    core_pts.append(round(
                        float(eval(str(team + '_win')).get(nick)[1]) * team_multis.get(team)[0] + float(
                            eval(str(team + '_lose')).get(nick)[1]) * team_multis.get(team)[1],
                        2))  # пофиксить на умножение
                    core_price.append(eval(team).get(nick)[2])
                elif eval(team).get(nick)[0] == 'S':
                    sup_nicks.append(nick)
                    sup_pts.append(round(
                        float(eval(str(team + '_win')).get(nick)[1]) * team_multis.get(team)[0] + float(
                            eval(str(team + '_lose')).get(nick)[1]) * team_multis.get(team)[1], 2))
                    sup_price.append(eval(team).get(nick)[2])

        for i in range(len(sup_nicks)):
            for j in range(i + 1, len(sup_nicks)):
                for k in range(len(core_nicks)):
                    for l in range(k + 1, len(core_nicks)):
                        for m in range(l + 1, len(core_nicks)):
                            score = round(sup_pts[i] + sup_pts[j] + core_pts[k] + core_pts[l] + core_pts[m], 2)
                            price = sup_price[i] + sup_price[j] + core_price[k] + core_price[l] + core_price[m]
                            if price <= 50:
                                setup1.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')',
                                               sup_nicks[j] + ' (' + str(sup_pts[j]) + ')',
                                               core_nicks[k] + ' (' + str(core_pts[k]) + ')',
                                               core_nicks[l] + ' (' + str(core_pts[l]) + ')',
                                               core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
                                if (checking_cores(core_nicks[k], core_nicks[l], core_nicks[m]) and (
                                checking_sups(sup_nicks[i],
                                              sup_nicks[j]))):  # and (core_nicks[l] or core_nicks[m]) in check_cores
                                    if (ex_sups(sup_nicks[i], sup_nicks[j]) and ex_cores(core_nicks[k], core_nicks[l],
                                                                                         core_nicks[m])):  #
                                        setup.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')',
                                                      sup_nicks[j] + ' (' + str(sup_pts[j]) + ')',
                                                      core_nicks[k] + ' (' + str(core_pts[k]) + ')',
                                                      core_nicks[l] + ' (' + str(core_pts[l]) + ')',
                                                      core_nicks[m] + ' (' + str(core_pts[m]) + ')'])

        setup_all1.sort(key=lambda i: i[0], reverse=True)
        setup.sort(key=lambda i: i[0], reverse=True)
        setup1.sort(key=lambda i: i[0], reverse=True)
        top_score = setup[0][0]
        setup = setup[0:10000]
        for i in range(len(setup)):
            setup[i].insert(1, round(setup[i][0] - top_score, 2))

        columns = ['Score', 'Diff', 'Price', 'Sup1', 'Sup2', 'Core1', 'Core2', 'Core3']
        self.ui.output_table.setColumnCount(len(columns))
        self.ui.output_table.setHorizontalHeaderLabels(columns)
        for record in range(len(setup)):
            self.ui.output_table.insertRow(record)
            for cell in range(len(setup[record])):
                self.ui.output_table.setItem(record, cell, QTableWidgetItem(str(setup[record][cell])))
        #self.ui.output_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        for col in range(0, 3):
            self.ui.output_table.resizeColumnToContents(col)
        for col in range(3, 8):
            self.ui.output_table.setColumnWidth(col, 130)


def deleting(sheet, players_list):
    global teams
    teams = []
    for player in sheet:
        if player.get('Team') not in teams:
            teams.append(player.get('Team'))
        if player.get('Score') != '' and player.get('Price') != 0:
            player['Score'] = str(player.get('Score')).replace(',', '.')
            player['Price'] = str(player.get('Price')).replace(',', '.')
        players_list.append([player.get('Team'), player.get('Player'),
                             [player.get('Role'), float(player.get('Score')), float(player.get('Price'))]])
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

# while True:
#     teams_with_score = []
#     for team in teams:
#         teams_with_score.append([team, 0, 0])
#     for team in teams:
#         temporary = locals()[str(team+'_win')]
#         locals()[str(team)] = temporary.copy()
#     playing = []
#     for x in range(len(teams)):
#         print(f"{x+1}: {teams[x]}\t")
#     who = input('Кто сегодня сыграет и как?\nВведите информацию в формате Index1 X - Y Index2;...: ')
#     # if who == "all":
#     #     playing = teams
#     who = who.split(';')
#     for match in who:
#         match = match.split(' - ')
#         for i in range(len(match)):
#             match[i] = match[i].split()
#             if i == 1:
#                 match[i].reverse()
#             teams_with_score[int(match[i][0])-1][1] += int(match[i][1])
#             teams_with_score[int(match[i][0])-1][2] += 2-int(match[i][1])
#             if teams[int(match[i][0])-1] not in playing:
#                 playing.append(teams[int(match[i][0])-1])
#
#     team_multis = {teamx[0]: teamx[1:] for teamx in teams_with_score}
#     # for f in range(len(who)):
#     #     playing.append(teams[int(who[f])-1])
#     del who
#     number = int(input('Сколько комбинаций нужно?: '))
#
#     sup_nicks = []
#     sup_price = []
#     sup_pts = []
#     core_nicks = []
#     core_price = []
#     core_pts = []
#     setup = []
#     setup1 = []
#     setup_all = []
#     setup_all1 = []
#
#     check_cores = []
#     check_sups = []
#     exclude_cores = []
#     exclude_sups = ['tOfu']
#
#     # match_data = teams_with_score дописать под добавление и умножение птс в словарь team
#     for team in playing:
#         nicks = eval(team).keys()
#         for nick in nicks:
#             if eval(team).get(nick)[0] == 'C':
#                 core_nicks.append(nick)
#                 core_pts.append(round(float(eval(str(team+'_win')).get(nick)[1])*team_multis.get(team)[0]+float(eval(str(team+'_lose')).get(nick)[1])*team_multis.get(team)[1], 2)) #пофиксить на умножение
#                 core_price.append(eval(team).get(nick)[2])
#             elif eval(team).get(nick)[0] == 'S':
#                 sup_nicks.append(nick)
#                 sup_pts.append(round(float(eval(str(team+'_win')).get(nick)[1])*team_multis.get(team)[0]+float(eval(str(team+'_lose')).get(nick)[1])*team_multis.get(team)[1], 2))
#                 sup_price.append(eval(team).get(nick)[2])
#
#     for i in range(len(sup_nicks)):
#         for j in range(i+1, len(sup_nicks)):
#             for k in range(len(core_nicks)):
#                 for l in range(k+1, len(core_nicks)):
#                     for m in range(l+1, len(core_nicks)):
#                         score = sup_pts[i] + sup_pts[j] + core_pts[k] + core_pts[l] + core_pts[m]
#                         price = sup_price[i] + sup_price[j] + core_price[k] + core_price[l] + core_price[m]
#                         if price <= 50:
#                             setup1.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')',
#                                            sup_nicks[j] + ' (' + str(sup_pts[j]) + ')',
#                                            core_nicks[k] + ' (' + str(core_pts[k]) + ')',
#                                            core_nicks[l] + ' (' + str(core_pts[l]) + ')',
#                                            core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
#                             if (checking_cores(core_nicks[k], core_nicks[l], core_nicks[m]) and (checking_sups(sup_nicks[i], sup_nicks[j]))): # and (core_nicks[l] or core_nicks[m]) in check_cores
#                                 if (ex_sups(sup_nicks[i], sup_nicks[j]) and ex_cores(core_nicks[k], core_nicks[l], core_nicks[m])): #
#                                     setup.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')', sup_nicks[j]+ ' (' + str(sup_pts[j]) + ')', core_nicks[k] + ' (' + str(core_pts[k]) + ')', core_nicks[l] + ' (' + str(core_pts[l]) + ')', core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
#
#     # sup_nicks = []
#     # sup_price = []
#     # sup_pts = []
#     # core_nicks = []
#     # core_price = []
#     # core_pts = []
#     #
#     # for team in teams:
#     #     nicks = eval(team).keys()
#     #     for nick in nicks:
#     #         if eval(team).get(nick)[0] == 'C':
#     #             core_nicks.append(nick)
#     #             core_pts.append(eval(team).get(nick)[1])
#     #             core_price.append(eval(team).get(nick)[2])
#     #         elif eval(team).get(nick)[0] == 'S':
#     #             sup_nicks.append(nick)
#     #             sup_pts.append(eval(team).get(nick)[1])
#     #             sup_price.append(eval(team).get(nick)[2])
#     #
#     # for i in range(len(sup_nicks)):
#     #     for j in range(i+1, len(sup_nicks)):
#     #         for k in range(len(core_nicks)):
#     #             for l in range(k+1, len(core_nicks)):
#     #                 for m in range(l+1, len(core_nicks)):
#     #                     score = sup_pts[i] + sup_pts[j] + core_pts[k] + core_pts[l] + core_pts[m]
#     #                     price = sup_price[i] + sup_price[j] + core_price[k] + core_price[l] + core_price[m]
#     #                     if price <= 50:
#     #                         # setup_all.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')',
#     #                         #                sup_nicks[j] + ' (' + str(sup_pts[j]) + ')',
#     #                         #                core_nicks[k] + ' (' + str(core_pts[k]) + ')',
#     #                         #                core_nicks[l] + ' (' + str(core_pts[l]) + ')',
#     #                         #                core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
#     #                         # if (checking_cores(core_nicks[k], core_nicks[l], core_nicks[m]) and (checking_sups(sup_nicks[i], sup_nicks[j]))): # and (core_nicks[l] or core_nicks[m]) in check_cores
#     #                         #     if (ex_sups(sup_nicks[i], sup_nicks[j]) and ex_cores(core_nicks[k], core_nicks[l], core_nicks[m])): #
#     #                                 setup_all1.append([score, price, sup_nicks[i] + ' (' + str(sup_pts[i]) + ')', sup_nicks[j]+ ' (' + str(sup_pts[j]) + ')', core_nicks[k] + ' (' + str(core_pts[k]) + ')', core_nicks[l] + ' (' + str(core_pts[l]) + ')', core_nicks[m] + ' (' + str(core_pts[m]) + ')'])
#
#     setup_all1.sort(key=lambda i: i[0], reverse=True)
#     setup.sort(key=lambda i: i[0], reverse=True)
#     setup1.sort(key=lambda i: i[0], reverse=True)
#     top_score = setup1[0][0]
#     setup = setup[0:number]
#     setup1 = setup1[0:number]
#     for i in range(len(setup)):
#         setup[i].insert(0, setup1.index(setup[i]))
#         setup[i].insert(2, setup[i][1]-top_score)
#
#     df = pd.DataFrame(setup, columns=['Orig Pos', 'Score', 'Diff', 'Price', 'Sup1', 'Sup2', 'Core1', 'Core2', 'Core3'])
#     pd.set_option('display.expand_frame_repr', False)
#     df = df.set_index('Orig Pos')
#     print(df)
#     del temporary
#     for team in teams:
#         del locals()[str(team)]

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
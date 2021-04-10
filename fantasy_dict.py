import pandas as pd
pd.set_option("display.min_rows", 200)
pd.set_option("display.max_rows", 999)

LGD = {'Ame': ['C', 17.846*2, 12.5], 'Faith bian': ['C', 13.475*2, 11], 'NothingToSay': ['C', 14.83*2, 11], 'Y`': ['S', 15.12*2, 9], 'XinQ': ['S', 13.19*2, 8.5]}
EG = {'Arteezy': ['C', 21.414, 12.5], 'Cr1t-': ['S', 17.54, 7.5], 'Fly': ['S', 18.77, 9.5], 'Iceiceice': ['C', 15.286, 9.5], 'Abed': ['C', 19.3, 12]}
IG = {'JT-': ['C', 11.04*2, 9.5], 'Kaka': ['S', 12.58*2, 9], 'Oli': ['S', 18.11*2, 9.5], 'Flyfly': ['C', 17.28*2, 11], 'Emo': ['C', 17.57*2, 12]}
Secret = {'MATUMBAMAN': ['C', 24, 15], 'Zai': ['C', 16.45, 10], 'Puppey': ['S', 24.65, 10.5], 'YapzOr': ['S', 21, 10], 'Nisha': ['C', 22.5, 14]}
Neon = {'Yopaj': ['C', 19.93, 10.5], 'Skemberlu': ['C', 20.03, 10], 'Jaunuel': ['S', 12.16, 10], 'PlayHard': ['C', 8.925, 9], 'Deth': ['S', 17.559, 7.5]}

VG = {'Ori': ['C', 14.24, 12], 'ELeVeN': ['C', 12.32, 9.5], 'Poyoyo': ['C', 21.96, 12], 'Pyw': ['S', 13.1, 9], 'Dy': ['S', 15.4, 10]}
TP = {'LeoStyle-': ['C', 20.14, 10], 'Mnz': ['C', 23.812, 10.5], 'Frank': ['C', 18.903, 7.5], 'MoOz': ['S', 13.67, 7], 'Mjz': ['S', 21.26, 8.5]}
VP = {'Gpk': ['C', 13.34, 13.5], 'Nightfall': ['C', 17.32, 15], 'Kingslayer': ['S', 9.52, 11.5], 'Save-': ['S', 16.8, 8.5], 'DM': ['C', 8.44, 10]}
Aster = {'Xxs': ['C', 10.976, 9], 'Monet': ['C', 21.416, 12], 'DD斩首': ['C', 14.232, 12.5], 'LaNm': ['S', 14.18, 8.5], 'Mad': ['S', 12.95, 7]}
QCY = {'CC&C': ['C', 16.158, 11.5], 'Lelis': ['C', 14.871, 10], 'YawaR': ['C', 19.124, 11.5], 'Poloson': ['S', 12.895, 8], 'SVG': ['S', 17.68, 9]}
Liquid = {'Boxi': ['C', 14.144, 8], 'Qojqva': ['C', 17.764, 11], 'MiCKe': ['C', 25.66, 12], 'Taiga': ['S', 14.15, 8.5], 'INSaNiA': ['S', 19.58, 9]}
Fnatic = {'DJ': ['S', 18.295, 10], 'Moon': ['C', 17.967, 10.5], 'Jabz': ['S', 16.795, 9.5], 'Raven': ['C', 24.961, 12.5], 'Masaros': ['C', 15.657, 9]}

sup_nicks = []
sup_price = []
sup_pts = []
core_nicks = []
core_price = []
core_pts = []
setup = []
setup1 = []

playing = [LGD, EG]

check_cores = []
check_sups = []
exclude_cores = []
exclude_sups = []

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


for team in playing:
    nicks = team.keys()
    for nick in nicks:
        if team.get(nick)[0] == 'C':
            core_nicks.append(nick)
            core_pts.append(team.get(nick)[1])
            core_price.append(team.get(nick)[2])
        if team.get(nick)[0] == 'S':
            sup_nicks.append(nick)
            sup_pts.append(team.get(nick)[1])
            sup_price.append(team.get(nick)[2])

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


setup.sort(key=lambda i: i[0], reverse=True)
setup1.sort(key=lambda i: i[0], reverse=True)
top_score = setup1[0][0]
for i in range(len(setup)):
    setup[i].insert(0, setup1.index(setup[i]))
    setup[i].insert(2, setup[i][1]-top_score)

df = pd.DataFrame(setup, columns=['Orig Pos', 'Score', 'Diff', 'Price', 'Sup1', 'Sup2', 'Core1', 'Core2', 'Core3'])
pd.set_option('display.expand_frame_repr', False)
df = df.set_index('Orig Pos')
print(df)
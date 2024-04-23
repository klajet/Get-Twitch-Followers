import os
import requests
import json
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# LANGUAGE = 0  # PL
LANGUAGE = 1    # ENG

client_id = 'YOUR+CLIENT_ID'
URI = 'http://localhost'
clientsecret = 'YOUR_CLIENT_SECRET'

streamer_name = "STREAMER_NAME"

r_p = ('https://id.twitch.tv/oauth2/token?client_id=' + client_id + '&client_secret=' + str(clientsecret) +'&grant_type=client_credentials')

print(r_p)

req_p = requests.post(r_p)

print(req_p)

print(req_p.json())

ans = req_p.json()

access_token = ans["access_token"]
expires_in = str(ans["expires_in"])
token_type = 'Bearer'

print(token_type + " " + access_token + " " + expires_in)

headers = {
    'Authorization': (token_type + ' ' + access_token),
    'Client-Id': client_id
}


URL = ('https://api.twitch.tv/helix/users?login=' + streamer_name)
print("URL: "+URL)
print("headers: "+str(headers))
req_g = requests.get(URL, headers=headers)

try:
    os.mkdir("files/"+streamer_name)
except:
    print("Directory Already Exists!")

print(req_g.json())

if (req_g):
    # print(req_g.json())

    ans = req_g.json()
    pack = ans["data"]
    dict = pack[0]
    streamer_id = dict["id"]
    login = dict["login"]
    print(streamer_id + " " + login)


URL = ('https://api.twitch.tv/helix/channels/followers?broadcaster_id=' + streamer_id + "&first=100")
req_g = requests.get(URL, headers=headers)

print(req_g)

if(req_g):
    print(req_g.json())

    answer = req_g.json()
    follow_amount = answer["total"]
    print(str(follow_amount) + "\n")
    cursor = ((req_g.json())["pagination"])["cursor"]

    to_file = open("files/"+streamer_name+"/"+"follow_list.txt", "w", encoding="utf8")

    data_dict = answer["data"]
    print(answer["data"])
    to_file.write(str(data_dict))

    while(cursor):
            URL = ('https://api.twitch.tv/helix/channels/followers?broadcaster_id=' + streamer_id + "&first=100" + "&after=" + cursor)
            req_g = requests.get(URL, headers=headers)
            # print(req_g.json())

            answer = req_g.json()
            data_dict = answer["data"]
            print(answer["data"])
            to_file.write("\n" + str(data_dict))
            try:
                cursor = ((req_g.json())["pagination"])["cursor"]
            except:
                cursor = 0
to_file.close()

print(" ~ Done 1! ~ ")


from_file = open("files/"+streamer_name+"/"+"follow_list.txt", "r", encoding="utf8")
to_file = open("files/"+streamer_name+"/"+"follow_list_parse.csv", "w", encoding="utf8")
to_file_increase = open("files/"+streamer_name+"/"+"follow_list_increase.csv", "w", encoding="utf8")

to_file.write("id,from_id,since\n\n")

for x in from_file:
    list = x.rstrip("\n")
    list = list.replace("'", "\"")
    print(list)
    d = json.loads(list)
    ifFirst = 0
    for y in d:
        since = (y["followed_at"])[:10]
        since_m = (y["followed_at"])[:7]
        to_file.write(y["from_id"] + "," + y["from_login"] + "," + since + "\n")
        to_file_increase.write(since_m + "\n")
        if(not ifFirst):
            last_m = since_m
            print(since_m)
            ifFirst = 1
        if(since_m != last_m):
            print(since_m)
        last_m = since_m

from_file.close()
to_file.close()
to_file_increase.close()

print(" ~ Done 2! ~ ")


to_file = open("files/"+streamer_name+"/"+"follow_increase.csv", "w", encoding="utf8")
from_file = open("files/"+streamer_name+"/"+"follow_list_increase.csv", "r", encoding="utf8")

sum_dict = []
dict = []

i = 0
j = 0
for x in from_file:
    x = x.rstrip("\n")
    if(i == 0):
        sum_dict.append(1)
        dict.append(x)
    else:
        if(x == dict[j]):
            print(dict[j] + " " + str(sum_dict[j]))
            # print(sum_dict[j])
            sum_dict[j] = sum_dict[j] + 1
        else:
            to_file.write(str(dict[j]) + "," + str(sum_dict[j]) + "\n")
            j = j + 1
            sum_dict.append(1)
            dict.append(x)

    i = i + 1

from_file.close()
to_file.close()

print(" ~ Done 3! ~ ")

from_file = open("files/"+streamer_name+"/"+"follow_increase.csv", "r", encoding="utf8")

date = []
am = []
avg = []
ranges = 0
sum_1 = 0
sum_2 = []

for x in from_file:
    x = x.strip("\n")
    if (x != ""):
        date.append(x[:7])
        am.append(int(x[8:]))

from_file.close()
ranges_1 = len(date)
print(am)
print(date)

for x in reversed(range(0, ranges_1)):
    sum_1 += am[x]
    sum_2.append(sum_1)
# sum_2.append(0)
sum_2.reverse()

# plt.autoscale()

EN_ylabel = "amount"
EN_xlabel = "year-month"
EN_title = "Followers increase "
EN_bar1 = "followers sum"
EN_bar2 = "New follows"
EN_filename = "Follow_increase "

PL_ylabel = "ilość"
PL_xlabel = "rok-miesiąc"
PL_title = "Przyrost obserwujących "
PL_bar1 = "suma obserwujących"
PL_bar2 = "nowi obserwujący"
PL_filename = "Przyrost_widzow_"

if (LANGUAGE == 0):
    LAN_ylabel = PL_ylabel
    LAN_xlabel = PL_xlabel
    LAN_title = PL_title
    LAN_bar1 = PL_bar1
    LAN_bar2 = PL_bar2
    LAN_filename = PL_filename
elif (LANGUAGE == 1):
    LAN_ylabel = EN_ylabel
    LAN_xlabel = EN_xlabel
    LAN_title = EN_title
    LAN_bar1 = EN_bar1
    LAN_bar2 = EN_bar2
    LAN_filename = EN_filename


f = plt.figure()
f.set_figwidth(len(am)/3)
plt.ylabel(LAN_ylabel)
plt.xlabel(LAN_xlabel)
plt.title(LAN_title + streamer_name)
plt.bar(date, sum_2, label=LAN_bar1, color='forestgreen')
plt.bar(date, am, label=LAN_bar2, color='lime')

plt.ylim(top=sum_1+(sum_1*0.10))
plt.legend()



plt.gca().invert_xaxis()
plt.xticks(rotation=90)

# , bbox_inches="tight"

plt.savefig("files/"+streamer_name+"/"+LAN_filename + streamer_name)
# plt.show()
plt.clf()

ranges = len(date)
sum = am[ranges - 1]
print(sum)
# avg.append(0)

for x in reversed(range(0, ranges)):
    avg.append(round((am[x] / sum) * 100, 2))
    sum += am[x]
avg.reverse()
print(len(avg))
print(len(date))

f = plt.figure()
f.set_figwidth(len(avg)/4)
plt.ylabel("%")
plt.xlabel(LAN_xlabel)
plt.title(LAN_title + streamer_name)
plt.bar(date, avg, color='g', align='center')
plt.gca().invert_xaxis()
plt.xticks(rotation=90)

plt.savefig("files/"+streamer_name+"/"+LAN_filename + "_2" + streamer_name)
#plt.show()

print("\nFollowers: "+str(follow_amount) + "\n")
print(" ~ Done All! ~ ")

#!/usr/bin/python

import sys
import json
import hashlib
import requests
import datetime

# sys.path.append("../lspylib")
# import baseinfo


# pageNum=1&pageSize=2000&source=SETTLE&key=19732634573454957456555634109238
#
# sign=A51E6E1A5D18A7763246FC15BF043EFA
key = "19732634573454957456555634109238"
#url = "http://yapi.lepass.cn/mock/1308/agent/account/all"
url = "https://t-banyanshare.lepass.cn/agent/account/all"

def sign_params_str(params):
    params_str =  "pageNum=" + str(params['pageNum']) + "&pageSize=" + str(params['pageSize']) + \
                  "&source=SETTLE&key=" + key
    # params_str ="pageNum=1&pageSize=2000&source=SETTLE&key=19732634573454957456555634109238"

    sign_str = hashlib.new('md5', bytes(params_str,encoding="utf8")).hexdigest().upper()
    print ("sign:" + sign_str)

    return sign_str

def get_request_url(params):
    sign_str = sign_params_str(params)

    request_url = url + "?pageNum=" + str(params['pageNum']) + "&pageSize=" + str(params['pageSize']) + \
                  "&source=SETTLE&sign=" + sign_str

    return request_url


if __name__ == '__main__':
    # lrb_agent_info = dict()
    # ret = baseinfo.init_lrb_all_agent_info(lrb_agent_info)
    # if ret != 0:
    #     print ("xx")
    #
    # print (lrb_agent_info)


    header_dict = {"Content-Type": "application/json; charset=utf8", "agentId": ""}
    params = dict()
    params['pageNum'] = 1
    params['pageSize'] = 10

    request_url = get_request_url(params)

    r = requests.get(request_url,headers=header_dict)
    print (r.text)
    dictinfo = json.loads(r.text)
    print (dictinfo)

    print("----------------------")
    print(dictinfo['returnCode'])
    print("----------------------")
    print(dictinfo['data']['total'])
    print("----------------------")

    if dictinfo['returnCode'] == '0':
        print(dictinfo['data'])
        print("----------------------")

        agent_li = dictinfo['data']['list']

        print(len(agent_li))

        lrb_agent_info = dict()
        for i in range(len(agent_li)):
            agent_dic = agent_li[i]
            print (agent_dic['agentId'])

            info = dict()
            info['F_agent_id'] = agent_dic['agentId']
            info['F_parent_agent_id'] = agent_dic['superAgentId']
            info['F_top_agent_id'] = agent_dic['topAgentId']
            info['F_agent_level'] = int(agent_dic['level'])
            info['F_agent_class'] = 19
            info['F_all_agent_id'] = ""
            lrb_agent_info[info['F_agent_id']] = info

        print("----------------------")
        print (lrb_agent_info)

    date = "2021-01-06"
    new = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    print (new)

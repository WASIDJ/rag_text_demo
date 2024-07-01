# -*- coding: utf-8 -*-
"""
Created on 2024/5/21 20:53
@author: Jeff Kafka  (23730105@sus.edu.cn)
"""
import requests
import parsel
import json
import re

urls_list = [
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=32872818&answerId=52936310&enc=47fc2d739afeef675b3e092eca9bdea0',
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=33165741&answerId=52957167&enc=cb54d8a0d05a19189739864f0872639f',
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=33806276&answerId=53012928&enc=1cdd31d019efacb618b1ad661fdcba41',
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=34050767&answerId=53037447&enc=14123be5b22b1f0f6348f2dbf5371c40',
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=34271388&answerId=53069120&enc=3ad172759cb06ec7191d13f838d96dd3',
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=34419591&answerId=53102319&enc=ea7ff60e5dfffff534cbc0bdaeec25b5',
    'https://mooc1.chaoxing.com/mooc-ans/mooc2/work/view?courseId=241382913&classId=93918097&cpi=339807669&workId=35021247&answerId=53199563&enc=9ad447653223be13743928172f051994'
]
# 设置url headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Cookie': 'lv=2; fid=1247; xxtenc=888cf5d3a6923ce475c75acb8e0e9263; wfwfid=1247; workRoleBenchId=0; siteType=2; createSiteSource=num8; _uid=293728811; uf=b2d2c93beefa90dcb7a96ffdb3fc364e15a58afd3124ae003e97a55e5d12a8b0e7a5b883da844cb803f0c0b62dd6e1ac913b662843f1f4ad6d92e371d7fdf64467c3000f6e78d08d8b6f06f3c6e4d776eea6be31981211d2480929d68092dda9b2017aab640ef9f0; _d=1716213509590; UID=293728811; vc=D4B0345962FBF3258FC4115AE6358A9C; vc2=907D6A1E2998164A564F5C9F8A320BF8; vc3=YthzZFOWcvg%2BgDT2nSPehIxfPIB8ef0nE0kCdUGD5%2BcMLu0bfI%2FEgFa3pPR9BdUw2Nxj%2FLm60d5Ygjtb1HSxu8vVRc2VFQgCOW6b%2BtgWJgb6MF8%2FySaJxHlPg1rJDO1M2A83z1UA0pA7c3zi1VN4F5nb2Ov6ffxeekdFvG2MVhE%3Df8e211ef4a6c9b529078e5d80110b1c0; cx_p_token=2f1d4ef3babda17119ca298c4ae78e54; p_auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyOTM3Mjg4MTEiLCJsb2dpblRpbWUiOjE3MTYyMTM1MDk1OTEsImV4cCI6MTcxNjgxODMwOX0.k4o7GPMxgnNRgd8b-nw4odCPOaKuRdE9PJYvFKzLOdY; DSSTASH_LOG=C_38-UN_1074-US_293728811-T_1716213509592; source=num2; wfwEnc=AA72467B6B12EC0411991A14845B784C; styleId=; spaceFid=1247; spaceRoleId=3; tl=1; k8s=1716213535.037.906.433198; route=5052ecf6e7d4195bf80fb406c3095b7d; _industry=5; 241382913cpi=339807669; 241382913ut=s; 241382913t=1716213534122; 241382913enc=41755eab3703312e2fc4f555b105e2c5; 241383440cpi=339807669; 241383440ut=s; 241383440t=1716215909534; 241383440enc=d375df70fa74fa7dfae4ae8dcdd1b99f; jrose=8B11CDA9A24B7279902178F52875FF6E.mooc-4241908859-481x1'
}
query_json = []
for url in urls_list:
    r = requests.get(url, headers=headers)
    print('status code :', r.status_code)

    selector = parsel.Selector(r.text)
    # 第一次提取
    data_list = selector.xpath('//div[@class="marBom60 questionLi singleQuesId"]')
    # 第二次筛选
    for data in data_list:
        # 获取问题

        question = re.findall(r'<h3 class="mark_name colorDeep" tabindex="0">(.*?)</h3>', str(data), flags=re.S)
        question = re.sub(r'<.*?>', '', question[0])  # 去除html标签
        #print('query:',question)
        # 获取选项
        choice_single = re.findall(r'<li tabindex="0">(.*?)</li>', str(data), flags=re.S)
        print('-' * 50)
        choice = [re.sub(r'<.*?>', '', choice_single[x]) for x in range(len(choice_single))]
        #print('chioce:',choice)

        query_json.append({
            'question': question,
            'choice':choice,
            'answers': '',
            'reference':''
        })
#写入json文件
json.dump(query_json,open('./大数据导论知识问答/question_list.json',mode='w',encoding='utf-8'),ensure_ascii=False)#ensure_ascii=False


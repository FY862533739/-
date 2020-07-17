import urllib
from urllib import parse
import requests
import re
from PIL import Image
from lxml import etree
import openpyxl

print("该程序获取的是教务系统中的历年成绩，暂不支持其他~")
def FindGrade():
    p1 = input("输入学号：")
    p2 = input("输入密码：")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    url = "http://172.16.0.30/default2.aspx"
    s = requests.session()
    r = s.get(url=url, headers=headers)
    html = r.text
    # 验证码
    cheakcode_url = re.findall(r'alt="看不清，换一张"\s?src="(.*?)"', html)[0]
    cheakcode_url = "http://172.16.0.30/"+cheakcode_url
    response2 = s.get(url=cheakcode_url, headers=headers)
    with open('code.jpg', 'wb') as fp:
        fp.write(response2.content)
    img = Image.open('code.jpg')
    img.show()
    try:
        p3 = input("输入验证码：")
        data = {
            "__VIEWSTATE": "/wEPDwULLTE4MTQyODExMTJkZAkHHQ2nmHGKx+x7Xm/qBk2jCNYP",
            "__EVENTVALIDATION": "/wEWDwK7vInHAgKl1bKzCQKM0rLrBgLs0fbZDAKEs66uBwK/wuqQDgKAqenNDQLN7c0VAuaMg+INAveMotMNAoznisYGArursYYIAt+RzN8IApObsvIHArWNqOoP9qsDKB8K4SZue8u9CTgb6RN06DU=",
            "txtUserName": p1,
            "Textbox1": "",
            "TextBox2": p2,
            "txtSecretCode": p3,
            "RadioButtonList1": "(unable to decode value)",
            "Button1": "",
            "lbLanguage": "",
            "hidPdrs": "",
            "hidsc": ""
            }
        response3 = s.post(url=url, data=data, headers=headers)
        str_xm = re.findall('<span\s?id="xhxm">(.*?)同学</span></em>', response3.text)
        str_xm2 = urllib.parse.quote(str_xm[0])  # 编码转化
        print(str_xm[0] + ":登陆成功")
        """请求并解析成绩页面的__EVENTVALIDATION和__VIEWSTATE两个参数"""
        url = "http://172.16.0.30/xscjcx.aspx?xh=" + p1 + "&xm=" + str_xm2 + "&gnmkdm=N121605"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            "Referer": "http://172.16.0.30/xs_main.aspx?xh=2017111728"
        }
        r = s.get(url=url, headers=headers)
        html = etree.HTML(r.text)
        __EVENTVALIDATION = html.xpath("//input[@id='__EVENTVALIDATION']/@value")
        __VIEWSTATE = html.xpath("//input[@id='__VIEWSTATE']/@value")
        data2 = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__EVENTVALIDATION": __EVENTVALIDATION,
            "__VIEWSTATE": __VIEWSTATE[0],
            "hidLanguage": "",
            "ddlXN": "",
            "ddlXQ": "",
            "ddl_kcxz": "",
            "btn_zcj": "(unable to decode value)"
        }
        r = s.post(url=url, headers=headers, data=data2)
        res = re.findall("<td>(.*?)</td>", r.text)
        ts = res[15:]
        ts = [' ' if i == '&nbsp;' else i for i in ts]
        step = 15
        b = [ts[i:i + step] for i in range(0, len(ts), step)]
        sheet_header = ["学年", "学期", "课程代码", "课程名称", "课程性质", "课程归属", "学分", "绩点", "成绩", "辅修标记", "补考成绩", "重修成绩", "开课学院", "备注",
                        "重修标记"]
        wb = openpyxl.Workbook()
        sheet_f = wb.active
        sheet_f["A1"] = sheet_header[0]
        sheet_f["B1"] = sheet_header[1]
        sheet_f["C1"] = sheet_header[2]
        sheet_f["D1"] = sheet_header[3]
        sheet_f["E1"] = sheet_header[4]
        sheet_f["F1"] = sheet_header[5]
        sheet_f["G1"] = sheet_header[6]
        sheet_f["H1"] = sheet_header[7]
        sheet_f["I1"] = sheet_header[8]
        sheet_f["J1"] = sheet_header[9]
        sheet_f["K1"] = sheet_header[10]
        sheet_f["L1"] = sheet_header[11]
        sheet_f["M1"] = sheet_header[12]
        sheet_f["N1"] = sheet_header[13]
        sheet_f["O1"] = sheet_header[14]
        for i in b:
            sheet_f.append(i)
        wb.save(str_xm[0] + "成绩表" + ".xlsx")
        print("成绩已下载至当前目录下")
    except:
        hint = re.findall("alert\('(.*?)'\)", response3.text)[0]  # 错误提示
        print("遇到错误：%s" % hint)
if __name__ == "__main__":
    while True:
        FindGrade()
        print("{:~^50}".format("继续?"))











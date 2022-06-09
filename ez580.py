import time
import json
import requests

money = 0


def Costing():
    global money
    error_item = []
    print("输入需要查询的物品:")
    while True:
        s = input().strip().replace("x", "*")
        # print(s)
        if s.startswith(
            (
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
            )
        ):  # 判断是否数字开头
            s1 = s.split("*")
            s = (
                s1[0]
                .replace("1", "一", 1)
                .replace("2", "二", 1)
                .replace("3", "三", 1)
                .replace("4", "四", 1)
                .replace("5", "五", 1)
                .replace("6", "六", 1)
            )  # 防止出现数字开头无法识别
            if len(s1) == 2:
                s = s + "*" + s1[1]
            else:
                s = s
        try:
            if s == "q":
                break
            with open("items_price.txt", "r", encoding="utf-8") as f:
                exec(f.read())
                # print(f.read())
                money += int(eval(s))

        except:
            c = s.split("*")
            error_item.append(c[0].strip())
    with open("items_price.txt", "a", encoding="utf-8") as f:
        for i in error_item:
            f.write(i.strip() + "=0" + "\n")

    print("物品成本:", money, "\n 未识别物品", error_item)


def Query_get(itemid_str):
    print("正在查询物品价格")
    try:
        cx_url = "https://universalis.app/api/v2/ShenYiZhiDi/{}?listings=1&entries=1&hq=nq".format(
            itemid_str
        )
        items_price = requests.get(cx_url)
        t = items_price.text
        js = json.loads(t)
        return js
    except json.decoder.JSONDecodeError:
        Query_get(itemid_str)


def Query(x):
    items = []
    with open("items_price.txt", "r", encoding="utf-8") as f:
        while True:
            item = f.readline()
            if not item:
                break
            if "=0" not in item and x == 2:
                continue
            item = item.split("=")
            items.append(item[0].strip())
    # print(items)
    count = 1
    item_15_list = []
    js_list = []
    if not items:
        print("无增量")
        return 1

    for i in items:
        i = (
            i.strip()
            .replace("一", "1", 1)
            .replace("二", "2", 1)
            .replace("三", "3", 1)
            .replace("四", "4", 1)
            .replace("五", "5", 1)
            .replace("六", "6", 1)
        )
        # print(i)
        if count == 15:
            js_list.append(Query_get(item_to_id(item_15_list)))
            item_15_list = []
            # exit()
            time.sleep(3)
            count = 1
        item_15_list.append(i)
        count += 1
    js_list.append(Query_get(item_to_id(item_15_list)))
    # print(js_list)
    save(js_list, x)


save_dict = {}


def save(js_list, x):
    print("正在保存")
    if x == 1:
        with open("items_price.txt", "w", encoding="utf-8") as f:
            for i in js_list:
                if "itemIDs" in i:
                    for j in i["itemIDs"]:
                        jiage = i["items"][str(j)]["minPrice"]
                        str_r = save_dict.get(str(j)) + "=" + str(jiage)
                        f.write(str_r + "\n")
                else:
                    jiage = i["minPrice"]
                    str_r = save_dict.get(str(i["itemID"])) + "=" + str(jiage)
                    f.write(str_r + "\n")

        print("保存完成")
    elif x == 2:
        with open("items_price.txt", "r", encoding="utf-8") as f:
            lines = f.read()
        with open("items_price.txt", "w", encoding="utf-8") as f_w:
            for i in js_list:
                # print(i)
                if "itemIDs" in i:
                    for j in i["itemIDs"]:
                        jiage = i["items"][str(j)]["minPrice"]
                        str_r = str(save_dict.get(str(j))) + "=" + str(jiage)
                        # print(str_r) 获取增量查询的价格
                        qs = str(save_dict.get(str(j)))
                        lines = lines.replace(qs + "=0", str_r)
                else:
                    jiage = i["minPrice"]
                    # print(jiage)
                    # print(save_dict)
                    # print(i["itemID"])
                    str_r = str(save_dict.get(str(i["itemID"]))) + "=" + str(jiage)
                    # print(str_r)
                    qs = str(save_dict.get(str(i["itemID"])))
                    lines = lines.replace(qs + "=0", str_r)
            f_w.write(lines)
            print("保存完成")


def item_to_id(item_15_list):
    itemid_str = str()
    with open("id.txt", "r", encoding="utf-8") as f:
        while True:
            t = f.readline()
            if not t:
                break
            a = t.split("=")
            if a[0].strip() in item_15_list:
                save_dict.update(
                    {
                        a[1]
                        .strip(): a[0]
                        .strip()
                        .replace("1", "一", 1)
                        .replace("2", "二", 1)
                        .replace("3", "三", 1)
                        .replace("4", "四", 1)
                        .replace("5", "五", 1)
                        .replace("6", "六", 1)
                    }
                )
                itemid_str += a[1].strip() + ","
    # print(save_dict)
    return itemid_str[:-1]


def main():
    while True:
        global money
        money = 0
        print(
            """
------请选择需要使用的功能------
1:成本计算
2:物品价格更新
q:退出
----------------------------"""
        )
        user_choose = input("请输入数字选择:")
        if user_choose == "q":
            break
        if user_choose == "1":
            Costing()
        elif user_choose == "2":
            while True:
                query_choose = input("请选择是全部查询(1)还是增量查询(2)(输入q退出):")
                if query_choose == "q":
                    break
                if query_choose == "1":
                    Query(1)
                    break
                elif query_choose == "2":
                    Query(2)
                    break
                else:
                    print("请重新输入。")
        else:
            continue


if __name__ == "__main__":
    main()

import pymysql
import re

db = pymysql.connect(host="localhost", user="root", password="Lyz3714Mrxh", database="test01")

cursor = db.cursor()
print("请输入操作")


while True:
    patterns = re.split(r'\s+', input())
    sql = ""

    if patterns[0] == 'ADD' or patterns[0] == 'add':
        if len(patterns) != 5:
            print("操作输入错误，请输入下一步操作或输入 EXIT 退出程序")
        else:
            sql = "insert into DEVICE VALUES ('%s', '%s', '%s', '%s')" % (patterns[1], patterns[2], patterns[3],patterns[4])
        
            try:
                cursor.execute(sql)
                db.commit()
                print("添加完毕，请输入下一步操作或输入 EXIT 退出程序")
            except:
                db.rollback()
            

    elif patterns[0] == 'DEL'or patterns[0] == 'del':
        sql1 = "delete from DEVICE where device_id='%s'" % patterns[1]
        sql2 = "select * from DEVICE where device_id='%s'" % patterns[1]
        if len(patterns) != 2:
            print("操作输入错误，请输入下一步操作或输入 EXIT 退出程序")
        else:    
            try:
                cursor.execute(sql2)
                result = cursor.fetchall()
                if result[0] == '':
                    print("找不到该设备，请输入下一步操作或输入 EXIT 退出程序")
                else:
                    try:
                        cursor.execute(sql1)
                        db.commit()
                        print("删除完毕，请输入下一步操作或输入 EXIT 退出程序")
                    except:
                        db.rollback()
                        print("出现错误，请输入下一步操作或输入 EXIT 退出程序")
            
            except:
                print("Error: Unable to fetch data.")
                print("请输入下一步操作或输入 EXIT 退出程序")
        

    elif patterns[0] == 'GET'or patterns[0] == 'get':
        if len(patterns) == 2:
            sql = "select * from DEVICE where device_id='%s'" % patterns[1]
        elif len(patterns) == 1:
            sql = "select * from DEVICE"
        else:
            print("操作格式错误")
            
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            if result[0] == '':
                print("找不到该设备，请输入下一步操作或输入 EXIT 退出程序")
            else:
                for row in result:
                    print("id='%s', name='%s', type='%s', state='%s'" % (row[0], row[1], row[2], row[3]))
                print("查询完毕，请输入下一步操作或输入 EXIT 退出程序")
                
            
        except:
            print("Error: Unable to fetch data.")
            print("请输入下一步操作或输入 EXIT 退出程序")

    elif patterns[0] == 'EXIT'or patterns[0] == 'exit':
        print("已退出程序")
        break
        
    else:
        print("操作输入错误，请输入下一步操作或输入 EXIT 退出程序")


db.close()

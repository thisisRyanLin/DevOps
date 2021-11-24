import csv
import getopt
import json
import sys
import os

def main(argv):
    inputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hp:b:", ["ifile="])
    except getopt.GetoptError:
        print ("python convert.py [-p|-b] <filename>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ("python3 convert.py [-p|-b] <filename>")
            sys.exit()
        elif opt in ("-p", "--ifile"):
            # 读json，创建csv
            jsonfile = open(arg, 'r', encoding = 'utf8')
            csvfile = open(arg[:-5]+'.csv', 'w', newline = '')
        
            json_dict = json.load(jsonfile)
        
            # 表头
            csv.writer(csvfile).writerow(json_dict[0].keys())
        
            # 内容
            for i in range(len(json_dict)):
                csv.writer(csvfile).writerow(json_dict[i].values())
            
            # 关闭文件
            jsonfile.close()
            csvfile.close()
            
        elif opt in ("-b", "--ifile"):
            # 读csv，创建json
            csvfile = open(arg, 'r', newline = '')
            jsonfile = open(arg[:-4]+'.json', 'w', encoding = 'utf8')
        
            # 读写
            json.dump(list(csv.DictReader(csvfile)), jsonfile)
        
            # close
            csvfile.close()
            jsonfile.close()
  

if __name__ == "__main__":
    main(sys.argv[1:])

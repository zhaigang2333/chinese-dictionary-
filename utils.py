import re
from collections import OrderedDict
import pymysql
from sqlalchemy import create_engine
import pandas as pd

#识别字符串中是否有汉字
def is_contain_chinese(check_str):
    """
    判断字符串中是否包含中文
    :param check_str: {str} 需要检测的字符串
    :return: {bool} 包含返回True， 不包含返回False
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False




#找到带〖符号的位置
def extract_and_count(arr):
    count = 0
    for i in range(len(arr)):
        if '〖' in arr[i]:
            break
        count += 1
        
    return count


#合并两个字符串数组，删除重复的字符串元素，并按照合并前的顺序排列
def merge_two_array(arr1,arr2):
    merged_arr = arr1 + arr2
    unique_ordered_dict = OrderedDict.fromkeys(merged_arr)
    merged_arr_no_duplicates = list(unique_ordered_dict.keys())
    return merged_arr_no_duplicates
#判断两个字符串数组是否有重复的元素
def is_contain_same_element(main_array,another_array):
    if not main_array or not another_array:
        return False
    
    last_element = main_array[-1]
    return last_element in another_array
#删除数组中另外一个数组的数据
def remove_elements_from_array(main_array, elements_to_remove):
    return [item for item in main_array if item not in elements_to_remove]
    return arr1
#替换数组中等于目标字符串的元素为空字符串
def replace_element_with_empty(arr, target_string):
    
    return ["@" if item == target_string else item for item in arr]
    
#向数据库中插入二维数组

def insert_data_into_db(data_array, db,host='192.168.21.40', port=3306, user='root', password='zg123456'):
    connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
       
        with connection.cursor() as cursor:
            # 假设数据表名为 'my_table'
            sql = "INSERT INTO xhzd_zici (id, zici, pinying, jiexi) VALUES (%s, %s, %s, %s)"  # 根据数据表结构修改
            values_list = [(item['id'], item['zici'], item['pinying'], item['jiexi']) for item in data_array]
            
            cursor.executemany(sql, values_list)
            connection.commit()
    except Exception as e:
        error_message = f"Error occurred when inserting data into database: {e}"
        print(error_message)
        write_to_txt_file("error_log.txt", error_message)
    finally:
        connection.close()

#查询数据库
def getdata_from_db(query, db, host='192.168.21.40', port=3306, user='root', password='zg123456'):
    try:
        engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8')
        # 使用 with 语句自动管理连接的生命周期
        with engine.connect() as conn:
            data = pd.read_sql(query, conn)
        return data
    except Exception as e:
        print(f"Error occurred when executing SQL query: {e}")
        return None

#转换成字典
def convert_to_custom_dict(input_array):
    keys = ['id', 'zici', 'pinying', 'jiexi']
    custom_dict = {keys[i]: input_array[i] for i in range(len(keys))}
    return custom_dict
def write_to_txt_file(filename, content):
    with open(filename, "a") as file:
        file.write(content + "\n")

def convert_data_to_string(data_array):
    result = ""
    for item in data_array:
        result += f"{'-' * 10}\n"
        result += f"ID: {item['id']}\n"
        result += f"Zici: {item['zici']}\n"
        result += f"Pinying: {item['pinying']}\n"
        result += f"Jiexi: {item['jiexi']}\n"
    return result
#判断字符串第一个和最后一个符号分别是不是()或者（）
def check_first_last_parentheses(input_string):
    if not input_string:
        return False
    
    first_char = input_string[0]
    last_char = input_string[-1]
    
    return (first_char == '(' and last_char == ')') or (first_char == '（' and last_char == '）') or (first_char == '[' and last_char == ']')


if __name__ == '__main__':
    #测试extract_and_count函数
    a1= ['乌', '烏', 'wū', '【形】', '浅黑色〖black;dark〗', '身披乌衣,手执耒耜,以率将士。——《三国志·邓艾传》', '又如:乌衣(黑衣);乌巾(黑头巾);乌丸(墨的别名);乌油(黑而光润);乌麻(黑芝麻)', '又如:乌有此事?', '乌', '烏', 'wū', '【叹】', '也作“於”。表示感叹']
    a2=['〖blackclouds;darkclouds〗∶黑云', '狂风四起,乌云满天', '〖blackhair〗∶借指妇女的乌发']
    print(merge_two_array(a1,a2))
    print(is_contain_same_element(a1,a2))
    print(remove_elements_from_array(a1,a2))
    print(replace_element_with_empty(a1,'乌'))
    arr=[[340, '@', 'jiǎn', '【动】,。本作“前”,通作“翦”,俗作“剪”〖cut;shear;trim〗(形声。从刀,前声。本义:用剪刀铰断)|剪,齐断也。——《说文》|勿剪勿伐。——《诗·召南·甘棠》|又如:剪截铺(衣料店); \
         剪筒(存放剪掉的蜡花的用具);剪直(直截了当,径直);剪断(亦作“简断”。利落,不啰嗦);剪鬃(剪去颈后的长毛。指短发)'], [340, '*', '*', '砍伐;截断〖cut〗', '松柏不剪。——南朝梁·丘迟《与陈伯之书》', '又如:剪伐(砍伐;割刈);剪断(切断,打断);剪边(夺取别人所爱的妓女)'], [340, '*', '*', '除灭。杀戮〖eliminate;kill〗', '此文王之所以止殃剪妖也。——《吕氏春秋·制乐》', '又如:剪屠(大肆杀戮);剪覆(全部消灭);剪弃(除去);剪落(削除);剪迹(犹灭迹)'], [340, '*', '*', '两手交叉〖crosshands〗。如:反剪着手;剪手就缚;剪缚(倒背双手捆绑起来)'], [340, '*', '*', '拦截〖intercept〗', '小人只在此大树坡剪径。——《水浒传》', '又如: \
剪江(在江中破浪而行);剪径强人(劫路的强盗);剪手(拦路抢劫的强盗)'], [340, '*', '*', '扫;挥动〖brandish〗', '林冲把朴刀杆剪了一下,蓦地跳将出来。——《水浒全传》', '剪尾能惊獐鹿,咆哮吓杀狐狸。——《三遂平\
妖传》'], [340, '*', '*', '辩白,驳斥〖offeranexplanation;refute〗', '张千、李万说一句,妇人就剪一句,妇人说得句句有理,张千、李万抵搪不过。——《古今小说》'], [340, '@', 'jiǎn', '【名】,交刀,剪刀〖scissors〗|断恨并州无快剪,牵愁织女少长丝。——清·孙枝蔚《思春辞》|又如:磨剪;剪简(放蜡花的工具)'], [340, '*', '*', '形状像剪刀的东西〖scissor-shapedtool〗。如:火剪;夹剪;烛剪'], [340, '剪报', 'jiǎnbào', '〖\
clip;newspaperclippings;newspapercuttings〗从报刊、杂志等上剪下的文字、图片资料'], [340, '剪裁', 'jiǎncái', '〖tailor〗∶把衣料按一定尺寸剪开|〖prune〗∶比喻对事物、材料的取舍安排|剪裁得当'], [340, '剪彩', 'jiǎncǎi', '〖cuttheribbonatanopeningceremony;cuttheribbonataspecialoccasion〗在仪式上剪断彩带,表示建筑物落成、新造车船出厂或展览会开幕等'], [340, '剪草除根', 'jiǎncǎo-chúgēn', '〖mowthegrassandpullouttheroots;cuttheweedsanddiguptheroots;destroyevil,leavingnochanceofitsrevival〗锄草要除掉根端,比喻除恶务尽,不能姑息遗患'], [340, '剪除', 'jiǎnchú', '〖wipeout;onnihilate;exterminate〗从根\
上去掉;消灭|剪除奸宄'], [340, '剪刀', 'jiǎndāo', '〖scissors〗切断布、纸、绳等东西用的铁制用具,两刃交错,可以开合'], [340, '剪刀差', 'jiǎndāochā', '〖scissorsmovementofprices;pricescissors;scissorsdifferenceinpricesbetweenindustrialgoodsandagriculturalproducts〗指工业产品与农业产品价格之间的差额,一般工业产品价格比农业产品价格高'], [340, '剪短', 'jiǎnduǎn', '〖crop〗把…剪得短些|这些印第安人将 \
他们的头发剪短到眼眉上面,后面齐到后颈'], [340, '剪发', 'jiǎnfà', '〖round〗剪短〖人〗的头发|剪发杜门。——明·张溥《五人墓碑记》'], [340, '剪辑', 'jiǎnjí', '〖filmediting;montage〗∶删剪、编排拍摄好的 \
镜头,使成为完整的影片。也作“剪接”|〖editingandrearrangement〗∶从总体中删去一部分,并把余下的重新编排;亦指经过删、编的成品'], [340, '剪接', 'jiǎnjiē', '〖cut〗剪辑〖影片〗'], [340, '剪径', 'jiǎnjìng', '〖(ofrobbers)holduptravellers〗拦路抢劫|走小路,多大虫,又有乘势夺包裹的剪径贼人。——《水浒传》'], [340, '剪口', 'jiǎnkǒu', '〖recess〗中国术语。扬州评话等曲种称一场演出终止处将书的内容剪断打住为剪\
口'], [340, '剪灭', 'jiǎnmiè', '〖wipeout〗铲除,消灭|剪灭恶霸'], [340, '剪票', 'jiǎnpiào', '〖punchaticket〗查票时用钳子状的器具把车票边沿剪出缺口'], [340, '剪切', 'jiǎnqiē', '〖shearing〗指依靠剪 \
切力分开材料'], [340, '剪书', 'jiǎnshū', '〖terminationofperformance〗中国曲艺术语。苏州评弹等曲种称演员在某地或某书场一个时期演出结束,为剪书'], [340, '剪贴', 'jiǎntiē', '〖clipandpaste〗∶把文字\
图片等剪下来,贴在别的纸上|〖cuttingout〗∶用彩色纸剪成人或东西的形象,贴在纸或别的东西上'], [340, '剪影', 'jiǎnyǐng', '〖sketch;paper-cutsilhouette〗∶把纸剪成人头、人体的轮廓形象|〖outline〗∶比喻对事\
物作轮廓的描写;亦指比喻描写出的轮廓'], [340, '剪纸', 'jiǎnzhǐ', '〖paper-cut〗一种民间工艺,用纸剪或刻成人物、花草、虫鱼、鸟兽等形象。也指剪成或刻出的工艺品'], [340, '剪子', 'jiǎnzi', '〖scissors;ctippers;scissors〗即剪刀,剪切东西时用']],
    
    data_array = [
    {'id': 340, 'zici': '@', 'pinying': 'jiǎn', 'jiexi': '【动】,。本作“前”,通作“翦”...'},
    {'id': 341, 'zici': '*', 'pinying': '*', 'jiexi': '砍伐;截断...'},
    {'id': 342, 'zici': '*', 'pinying': '*', 'jiexi': '除灭。杀戮...'}
    ]
    insert_data_into_db(data_array, 'dict')
    #print(convert_to_custom_dict([340, '*', '*', '辩白,驳斥〖offeranexplanation;refute〗', '张千、李万说一句,妇人就剪一句,妇人说得句句有理,张千、李万抵搪不过。——《古今小说》']))
    arr2= ['丰富', 'fēngfù', '〖rich;abundant;plentiful〗∶种类多,数量大', '资源丰富', '〖luxuriant〗∶极为多彩的']
    arr3=['〖rich;abundant;plentiful〗∶种类多,数量大', '资源丰富', '〖luxuriant〗∶极为多彩的', '丰富的神话', '〖plump〗∶充裕的,很多的;涉及面广的']
    a=['过半数', 'guòbànshù', '〖morethanhalf〗∶超过总数的一半']
    b= ['〖morethanhalf〗∶超过总数的一半', '这个工厂过半数的工人是妇女', '〖majority〗∶多数,大多数,半数以上', '过半数的人同意这个计划']
    print(is_contain_same_element(a,b))
    #print(convert_data_to_string(data_array))
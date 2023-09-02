import re
import utils as UT

def find_elements_with_symbol(arr):
    
    result = []
    
    i = 0
    while i < len(arr):
        #print(UT.check_first_last_parentheses(arr[i-1]))
        if '〖' in arr[i] and UT.check_first_last_parentheses(arr[i-1]):
            arr.pop(i-1)
            i=i-1
            continue
        #print('处理arr:',i,len(arr),arr[i],arr[i].find('〖') )
        if '〖' in arr[i] and arr[i].find('〖')==0 and has_chinese_character(arr[i])==False :         
            end_idx = i+1

            start_inx=i
            # Search forward until a symbol is found
            while end_idx < len(arr) and '〖'  in arr[end_idx] and  arr[end_idx]!='' : 
                end_idx = end_idx+1

            combined_elements = '|'.join(arr[start_inx-2:end_idx])
            #print('处理arr----',combined_elements,result[-2:])
            result=UT.remove_elements_from_array(result,arr[i-2:end_idx])
            result.append(combined_elements)
            #print('每一次处理结果：',result)
            i = end_idx
        elif '〖' in arr[i]  and '【' in arr[i-1]:
            end_idx = i+1
            start_inx=i
            while end_idx < len(arr) and '〖'  in arr[end_idx] and  arr[end_idx]!='' : 
                end_idx = end_idx+1 
            if arr[i-4]=='@':
                combined_elements = '@'+'|'.join(arr[i-3:i-1])+'|'+arr[i-1]+',' +arr[i]+'|'.join(arr[i+1:end_idx])
            else:
                combined_elements = '|'.join(arr[i-3:i-1])+'|'+arr[i-1]+',' +arr[i]+'|'.join(arr[i+1:end_idx])
            result=UT.remove_elements_from_array(result,arr[start_inx-3:end_idx])
            result.append(combined_elements)
            i = end_idx
        else:
            
            # If no symbol is found, simply add the element to the result
            if arr[i].find('同本义')!=-1:
                if arr[i-5]=='@':
                    combined_elements='@'+arr[i-4]+'|'+arr[i-3]+'|'+arr[i-2]+','+arr[i].replace('同本义','')+arr[i-1]
                else:
                    combined_elements=arr[i-4]+'|'+arr[i-3]+'|'+arr[i-2]+','+arr[i].replace('同本义','')+arr[i-1]
                #'|'.join(arr[i-3:i+1])

                result=UT.remove_elements_from_array(result,arr[i-4:i+1])
                result.append(combined_elements)
            else:
 
                result.append(arr[i])
            i += 1
    
    return result
def combin_elements_with_symbol(arr):
    result = []

    i = 0
    while i < len(arr):
        if '〖' in arr[i]:
            #print('combin_elements_with_symbol----:',arr[i])
            end_idx = i+1

            # Search forward until a symbol is found
            while end_idx < len(arr) and '〖' not in arr[end_idx] and arr[end_idx]!=''and arr[end_idx]!='@':
                end_idx += 1

            # Concatenate the elements within the range (start_idx, end_idx) with a comma separator
            combined_elements = '|'.join(arr[i :end_idx])
            result.append(combined_elements)

            # Move the pointer to the next position after the range
            i = end_idx
        else:
            # If no symbol is found, simply add the element to the result
            #result.append(arr[i])
            i += 1

    return result

#判断字符串是否汉字
def has_chinese_character(text):
    if '〗' not in text:
        return False
    pattern = r'〖(.*?)〗'
    matches = re.findall(pattern, text)
    for char in matches[0]:
        if '\u4e00' <= char <= '\u9fff':

            return True
    return False


if __name__ == '__main__':

    # Input array


    input_array = ['乌鸦', 'wūyā', '〖crow〗一种鸟,嘴大而直,全身羽毛黑色,翼有绿光,多群居在树林中或田野间,以谷物、果实、昆虫为食物',
               '乌烟瘴气', 'wūyān-zhàngqì', '〖foulatmosphere;pandemoniumreignsthorought〗瘴气,原指热带地方山林中的湿热空气,过去被误认为瘴疠的病源。比喻空气污浊、秩序混乱或社会黑暗、风气不正',
               '乌药', 'wūyào', '〖linderaroot;rootofthree-nervedspicebush〗中药名。别名“台乌药”。为樟科植物乌药的根',
               '乌油油', 'wūyóuyóu', '〖jet-black〗形容黑而发亮', '乌油油的眼珠子', '乌有', 'wūyǒu', '〖nothing;naught〗虚幻;不存在',
               '乌有先生者,乌有此事也。——《史记·司马相如列传》', '梦当好处成乌有。——袁桷诗', '子虚乌有', '乌鱼', 'wūyú', '〖snakehead〗乌鳢',
               '乌云', 'wūyún', '〖blackclouds;darkclouds〗∶黑云', '狂风四起,乌云满天', '〖blackhair〗∶借指妇女的乌发', '乌云压顶', 'wūyún-yādǐng',
               '〖rampant〗比喻恶势力猖狂', '乌枣', 'wūzǎo', '〖smokedjujube〗∶烟熏的枣', '〖blackjujube〗∶成黑色的加工过的枣', '乌贼', 'wūzéi',
               '〖cuttlefish;inkfish〗乌贼科(十腕目)的十腕海洋头足类软体动物,身体椭圆形而扁平,口的边缘有十只带吸盘的腕足,体内有墨囊,用以放出黑色液体掩护逃跑。介壳已退化为骨质内壳,可入药',
               '', '乌', '烏', 'wù', '另见wū', '', '乌拉', 'wùla', '〖leatherbootslinedwithwulasedge〗东北地区冬天穿的用皮革制的鞋,里面垫乌拉草']

    #test has_chinese_character
    print(has_chinese_character('〖crow〗一种鸟,嘴大而直,全身羽毛黑色,翼有绿光,多群居在树林中或田野间,以谷物、果实、昆虫为食物'))
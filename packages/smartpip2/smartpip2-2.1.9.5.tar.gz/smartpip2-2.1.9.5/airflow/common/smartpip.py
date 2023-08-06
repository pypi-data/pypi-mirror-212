import os #line:2
import requests #line:3
import time #line:4
import json #line:5
import re #line:6
import subprocess #line:7
import logging #line:8
try :#line:10
    from kafka import KafkaConsumer ,TopicPartition #line:11
except :#line:12
    logging .warning ('you need pip install kafka-python')#line:13
os .environ ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'#line:15
requests .packages .urllib3 .disable_warnings ()#line:16
from airflow .settings import ETL_FILE_PATH ,KETTLE_HOME ,HIVE_HOME ,P_URL ,DATASET_TOKEN ,REFRESH_TOKEN #line:18
from airflow .utils .email import fun_email ,list_email #line:19
from airflow .common .datax import datax_cmdStr #line:20
from airflow .exceptions import SmartpipException #line:21
_OOO0OOOO0OOOOOOOO =f'{P_URL}/echart/dataset_api/?token={DATASET_TOKEN}&visitor=Airflow&type='#line:24
_OOO00O000O0OO00OO =f'{P_URL}/echart/refresh_ds/?token={REFRESH_TOKEN}&type='#line:25
_O0OOOO0O0O0OOOO0O =f'{P_URL}/dm/api/sync_tableQuality/?token={REFRESH_TOKEN}&project='#line:26
def smart_upload (OOOOOO00OO0OO000O ):#line:30
    OOOO0OOOOO0000O00 ,O000OO0O0OOO0O0OO =os .path .split (OOOOOO00OO0OO000O )#line:31
    O000OO0O0OOO0O0OO =O000OO0O0OOO0O0OO .split ('.')[0 ]#line:32
    O0O0OO0O00O0OO000 ={"title":O000OO0O0OOO0O0OO ,"token":DATASET_TOKEN ,"visitor":"Airflow"}#line:37
    O00OOO00O000OO0O0 ={'file':open (OOOOOO00OO0OO000O ,'rb')}#line:38
    O0OOOOO000000OO0O =f'''{P_URL}/echart/dataset_api/?type=uploadlog&visitor=Airflow&token={DATASET_TOKEN}&param={{"uptime":"{time.time()}","filename":"{O000OO0O0OOO0O0OO}"}}'''#line:39
    OOO00O000OO00O000 =60 #line:40
    OO0OOO00OOO0000O0 =requests .post (f'{P_URL}/etl/api/upload_file_api/',files =O00OOO00O000OO0O0 ,data =O0O0OO0O00O0OO000 ,verify =False )#line:42
    print (OO0OOO00OOO0000O0 .status_code )#line:43
    if OO0OOO00OOO0000O0 .status_code ==200 :#line:44
        OO0OOO00OOO0000O0 =OO0OOO00OOO0000O0 .json ()#line:45
    elif OO0OOO00OOO0000O0 .status_code ==504 :#line:46
        print ('timeout, try waiting...')#line:47
        OO0OOO00OOO0000O0 ={"result":"error","data":"time out"}#line:48
        for O0OOOOOO00O0OOOO0 in range (20 ):#line:49
            O0000000OO00O0000 =requests .get (O0OOOOO000000OO0O ,verify =False ).json ()#line:50
            print (O0000000OO00O0000 )#line:51
            O0O0OO0O00O0OO000 =O0000000OO00O0000 ['data']#line:52
            if len (O0O0OO0O00O0OO000 )>1 :#line:53
                OO0OOO00OOO0000O0 ={"result":"success","data":"uploaded"}#line:54
                break #line:55
            time .sleep (OOO00O000OO00O000 )#line:56
    else :#line:57
        OO0OOO00OOO0000O0 ={"result":"error","data":"some thing wrong"}#line:58
    print (OO0OOO00OOO0000O0 )#line:59
    if OO0OOO00OOO0000O0 ['result']=='error':#line:60
        raise SmartpipException ('Upload Error')#line:61
def get_dataset (O000OO0OO0OO0O0OO ,param =None ):#line:64
    ""#line:70
    O0O0O0OOOO0000OOO =_OOO0OOOO0OOOOOOOO +str (O000OO0OO0OO0O0OO )#line:71
    if param :#line:72
        O0O0O0OOOO0000OOO =f'{O0O0O0OOOO0000OOO}&param={json.dumps(param)}'#line:73
    OOO00000OO00OOOO0 =requests .get (O0O0O0OOOO0000OOO ,verify =False )#line:74
    OOO00000OO00OOOO0 =OOO00000OO00OOOO0 .json ()#line:75
    return OOO00000OO00OOOO0 #line:76
def dataset (O0O00OOOO0OOOO0O0 ,OO0O0000OOO0O0O00 ,OOO0OOO00OO0O0O0O ,tolist =None ):#line:79
    ""#line:86
    O00OOOOO00OO000OO =60 *15 #line:87
    O0OOO0000OOOO0OO0 =3600 *2 #line:88
    O0OOO000O00O00OO0 =''#line:89
    try :#line:90
        while True :#line:91
            O0O000OO00OOO0O0O =requests .get (_OOO0OOOO0OOOOOOOO +OO0O0000OOO0O0O00 ,verify =False )#line:92
            O0O000OO00OOO0O0O =O0O000OO00OOO0O0O .json ()#line:93
            OOO00O00OOO0O00OO =O0O000OO00OOO0O0O ['result']#line:94
            O0O000OO00OOO0O0O =O0O000OO00OOO0O0O ['data']#line:95
            if OOO00O00OOO0O00OO =='error':#line:96
                raise Exception (f'{O0O000OO00OOO0O0O}')#line:97
            O0OOO000O00O00OO0 =',\n'.join ([str (O0000O00O0000OO00 )for O0000O00O0000OO00 in O0O000OO00OOO0O0O ])#line:98
            print (f'Dataset: {O0OOO000O00O00OO0} ')#line:99
            if OOO0OOO00OO0O0O0O =='e3':#line:100
                if len (O0O000OO00OOO0O0O )<2 :#line:101
                    if O0OOO0000OOOO0OO0 <=0 :#line:102
                        raise Exception ('超时且数据为空')#line:103
                    else :#line:104
                        time .sleep (O00OOOOO00OO000OO )#line:105
                        O0OOO0000OOOO0OO0 =O0OOO0000OOOO0OO0 -O00OOOOO00OO000OO #line:106
                else :#line:107
                    break #line:108
            else :#line:109
                if len (O0O000OO00OOO0O0O )>1 :#line:110
                    if OOO0OOO00OO0O0O0O =='e1':#line:111
                        raise Exception ('有异常数据')#line:112
                    elif OOO0OOO00OO0O0O0O =='e2':#line:113
                        list_email (f'Info_{O0O00OOOO0OOOO0O0}',f'{O0O00OOOO0OOOO0O0}-Dataset Status',O0O000OO00OOO0O0O ,to_list =tolist )#line:114
                else :#line:115
                    if OOO0OOO00OO0O0O0O not in ['info','e1']:#line:116
                        O0OOO000O00O00OO0 ='数据为空'#line:117
                        raise Exception (O0OOO000O00O00OO0 )#line:118
                break #line:119
    except Exception as OOOO00O0OO0O000O0 :#line:120
        fun_email (f'{O0O00OOOO0OOOO0O0}-执行Dataset校验出错',O0OOO000O00O00OO0 ,to_list =tolist )#line:121
        raise SmartpipException (str (OOOO00O0OO0O000O0 .args ))#line:122
def refresh_dash (O0OO0O0OOOOOOOO0O ,O000OO0OOO00O0O0O ):#line:125
    ""#line:128
    try :#line:129
        OO0OOO000OO0O00OO =requests .get (f'{_OOO00O000O0OO00OO}{O000OO0OOO00O0O0O}',verify =False )#line:130
        OO0OOO000OO0O00OO =OO0OOO000OO0O00OO .json ()#line:131
        print (OO0OOO000OO0O00OO )#line:132
        O00O0OOO0O000OO00 =OO0OOO000OO0O00OO ['status']#line:133
        if O00O0OOO0O000OO00 !=200 :#line:134
            raise SmartpipException ('refresh_dash')#line:135
    except Exception as O00000000O0O0000O :#line:136
        fun_email (f'{O0OO0O0OOOOOOOO0O}-执行refresh出错',str (O00000000O0O0000O .args ))#line:137
        raise SmartpipException (str (O00000000O0O0000O .args ))#line:138
def refresh_quality (OO000000O0OO0OO00 ,OO0O00O00O0OOOOOO ,hours =1 ):#line:141
    ""#line:144
    try :#line:145
        O00OO00OO00O0OOOO =requests .get (f'{_O0OOOO0O0O0OOOO0O}{OO0O00O00O0OOOOOO}&hours={hours}',verify =False )#line:146
        O00OO00OO00O0OOOO =O00OO00OO00O0OOOO .json ()#line:147
        print (O00OO00OO00O0OOOO )#line:148
        O00OO0OO0OO0OOOO0 =O00OO00OO00O0OOOO ['status']#line:149
        if O00OO0OO0OO0OOOO0 !=200 :#line:150
            raise SmartpipException ('refresh_quality')#line:151
    except Exception as OOOOO0O000O00O0OO :#line:152
        fun_email (f'{OO000000O0OO0OO00}-执行refresh_quality出错',str (OOOOO0O000O00O0OO .args ))#line:153
        raise SmartpipException (str (OOOOO0O000O00O0OO .args ))#line:154
def dash_mail (OO000O00OOO0OOO0O ,O0000OO00OO00OO0O ,O0O0OO000OO0000OO ):#line:157
    ""#line:161
    if callable (O0000OO00OO00OO0O ):#line:162
        OOOOO0OOO00OO0000 =O0000OO00OO00OO0O ()#line:163
    else :#line:164
        OOOOO0OOO00OO0000 =O0000OO00OO00OO0O #line:165
    print (OOOOO0OOO00OO0000 )#line:166
    if isinstance (OOOOO0OOO00OO0000 ,str ):#line:167
        fun_email (OO000O00OOO0OOO0O ,OOOOO0OOO00OO0000 ,O0O0OO000OO0000OO )#line:168
    else :#line:169
        fun_email (OOOOO0OOO00OO0000 [0 ],OOOOO0OOO00OO0000 [1 ],O0O0OO000OO0000OO )#line:170
    print ('发送邮件成功!')#line:171
def run_bash (OO00OOO0OO0OO0O0O ):#line:175
    OO0OOOOO0O0O0O00O =''#line:176
    O0OOO00000O0O00OO =subprocess .Popen (OO00OOO0OO0OO0O0O ,stdout =subprocess .PIPE ,stderr =subprocess .STDOUT ,shell =True ,cwd =ETL_FILE_PATH )#line:177
    print ('PID:',O0OOO00000O0O00OO .pid )#line:178
    for OOOO000O00OOOOO00 in iter (O0OOO00000O0O00OO .stdout .readline ,b''):#line:179
        if O0OOO00000O0O00OO .poll ()and OOOO000O00OOOOO00 ==b'':#line:180
            break #line:181
        OOOO000O00OOOOO00 =OOOO000O00OOOOO00 .decode (encoding ='utf8')#line:182
        print (OOOO000O00OOOOO00 .rstrip ())#line:183
        OO0OOOOO0O0O0O00O =OO0OOOOO0O0O0O00O +OOOO000O00OOOOO00 #line:184
    O0OOO00000O0O00OO .stdout .close ()#line:185
    OOO00O00OO000O00O =O0OOO00000O0O00OO .wait ()#line:186
    print ('result code: ',OOO00O00OO000O00O )#line:187
    return OO0OOOOO0O0O0O00O ,OOO00O00OO000O00O #line:188
def run_python (OO0OO0O0000O000O0 ,OO0O0O00OOOOO000O ,dev =''):#line:191
    O0OOOOOO0O00OOOOO =OO0OO0O0000O000O0 .split ('/')#line:192
    _OO0O0O00O00OO0O00 ,OOOO00OOO0OO00OO0 =run_bash ('python %s %s'%(OO0OO0O0000O000O0 ,OO0O0O00OOOOO000O ))#line:193
    if OOOO00OOO0OO00OO0 !=0 :#line:194
        fun_email (f'{O0OOOOOO0O00OOOOO[-2]}/{O0OOOOOO0O00OOOOO[-1]}出错','python error')#line:195
        raise SmartpipException ('python error')#line:196
def run_dataxx (O0OO00000OOOO00OO ,O0OOOO0O0O0000000 ,dev =''):#line:200
    O0O00OOOOO000O0O0 =O0OO00000OOOO00OO .split ('/')#line:201
    if O0OOOO0O0O0000000 :#line:202
        O00000O00OO00OO00 =[f'-D{OO0O000OOOO0OOO0O}:{OOOOOOO00OOOOOOOO}'for OO0O000OOOO0OOO0O ,OOOOOOO00OOOOOOOO in O0OOOO0O0O0000000 .items ()]#line:203
        O0OOOOO0OOO0000O0 =' '.join (O00000O00OO00OO00 )#line:204
        O00O0000OO00OO0OO =[f'-p"{O0OOOOO0OOO0000O0}"',O0OO00000OOOO00OO ]#line:205
    else :#line:206
        O00O0000OO00OO0OO =[O0OO00000OOOO00OO ]#line:207
    OO0O0000O000OO0O0 =datax_cmdStr (O00O0000OO00OO0OO )#line:208
    _OO0O0O0OO0000O000 ,OOO0O00O0000OOOOO =run_bash (OO0O0000O000OO0O0 )#line:209
    if OOO0O00O0000OOOOO !=0 :#line:210
        fun_email (f'{O0O00OOOOO000O0O0[-2]}/{O0O00OOOOO000O0O0[-1]}出错','datax error')#line:211
        raise SmartpipException ('error')#line:212
def run_datax (OO0O00000O0OOO000 ,O0OOO000O0000O00O ,O00OO0OO00000O0OO ,OOOOO00OOO0O00OO0 ,dev =''):#line:215
    with open (OO0O00000O0OOO000 ,'r',encoding ='utf8')as O0O0OOOOOO0000O00 :#line:216
        O0OO0000O0000000O =readSqlstr (O0O0OOOOOO0000O00 .read ().strip (),para_dict =OOOOO00OOO0O00OO0 )#line:217
    O0OO0000O0000000O =O0OO0000O0000000O .split ('##')#line:218
    O0O0000O00000O00O ={}#line:219
    for O000OO0O0O0O0OO00 in O0OO0000O0000000O :#line:220
        OO0O0O0O00O0O0000 =O000OO0O0O0O0OO00 .find ('=')#line:221
        if OO0O0O0O00O0O0000 >0 :#line:222
            O0O0000O00000O00O [O000OO0O0O0O0OO00 [:OO0O0O0O00O0O0000 ].strip ()]=O000OO0O0O0O0OO00 [OO0O0O0O00O0O0000 +1 :].replace ('\n',' ').strip ()#line:223
    OOOO00000O00O0OOO =O0O0000O00000O00O .keys ()#line:224
    OOOOOO00O0O000000 =O0O0000O00000O00O .pop ('template')if 'template'in OOOO00000O00O0OOO else 'default'#line:225
    OOO00000O0O00O000 =O0O0000O00000O00O .get ('targetColumn')#line:226
    OOO0OO0OO00000000 =None #line:227
    if OOOOOO00O0O000000 .endswith ('hdfs'):#line:228
        OOO0OO0OO00000000 =O0O0000O00000O00O .pop ('hiveSql')if 'hiveSql'in OOOO00000O00O0OOO else None #line:230
        if not OOO0OO0OO00000000 :#line:231
            OOO0OO0OO00000000 =O0O0000O00000O00O .pop ('postSql')if 'postSql'in OOOO00000O00O0OOO else None #line:232
        if OOO00000O0O00O000 :#line:234
            OOO00000O0O00O000 =OOO00000O0O00O000 .split (',')#line:235
            OO00000000OOOOO0O =[]#line:236
            for O000OO0O0O0O0OO00 in OOO00000O0O00O000 :#line:237
                if ':'in O000OO0O0O0O0OO00 :#line:238
                    O000OO0O0O0O0OO00 =O000OO0O0O0O0OO00 .split (':')#line:239
                    OO00000000OOOOO0O .append ({"name":O000OO0O0O0O0OO00 [0 ].strip (),"type":O000OO0O0O0O0OO00 [1 ].strip ()})#line:240
                else :#line:241
                    OO00000000OOOOO0O .append ({"name":O000OO0O0O0O0OO00 .strip (),"type":"STRING"})#line:242
            O0O0000O00000O00O ['targetColumn']=json .dumps (OO00000000OOOOO0O )#line:243
    else :#line:244
        if OOO00000O0O00O000 :#line:245
            OOO00000O0O00O000 =[OOOOO00OOOOOO0O00 .strip ()for OOOOO00OOOOOO0O00 in OOO00000O0O00O000 .split (',')]#line:246
            O0O0000O00000O00O ['targetColumn']=json .dumps (OOO00000O0O00O000 )#line:247
        else :#line:248
            O0O0000O00000O00O ['targetColumn']='["*"]'#line:249
        if OOOOOO00O0O000000 .endswith ('starrocks'):#line:251
            if '.'in O0O0000O00000O00O ['targetTable']:#line:252
                O0O0000O00000O00O ['targetDB'],O0O0000O00000O00O ['targetTable']=O0O0000O00000O00O ['targetTable'].split ('.')#line:253
            else :#line:254
                O0O0000O00000O00O ['targetDB']='Test'#line:255
        else :#line:256
            if 'writeMode'not in OOOO00000O00O0OOO :#line:257
                O0O0000O00000O00O ['writeMode']='insert'#line:258
    if 'preSql'in OOOO00000O00O0OOO :#line:259
        O0O0000O00000O00O ['preSql']=json .dumps (O0O0000O00000O00O ['preSql'].strip ().split (';'))#line:260
    else :#line:261
        O0O0000O00000O00O ['preSql']=''#line:262
    if 'postSql'in OOOO00000O00O0OOO :#line:263
        O0O0000O00000O00O ['postSql']=json .dumps (O0O0000O00000O00O ['postSql'].strip ().split (';'))#line:264
    else :#line:265
        O0O0000O00000O00O ['postSql']=''#line:266
    O00O0O000O0O0OOO0 =OO0O00000O0OOO000 .split ('/')#line:267
    OOO0O00000OO0O000 =O00O0O000O0O0OOO0 [-1 ].split ('.')[0 ]#line:268
    with open (os .path .join (O00OO0OO00000O0OO ,'datax','templates',OOOOOO00O0O000000 ),'r')as O0O0OOOOOO0000O00 :#line:269
        OO000O0O000000OOO =O0O0OOOOOO0000O00 .read ()#line:270
    OO0O00000O0OOO000 =os .path .join (O00OO0OO00000O0OO ,'datax',OOO0O00000OO0O000 +'.json')#line:271
    with open (OO0O00000O0OOO000 ,'w',encoding ='utf8')as O0O0OOOOOO0000O00 :#line:272
        O0O0OOOOOO0000O00 .write (readSqlstr (OO000O0O000000OOO ,O0O0000O00000O00O ))#line:273
    O0O000000OO000OOO =datax_cmdStr ([OO0O00000O0OOO000 ])#line:274
    _O0OOOO0OOOOOOO000 ,O00O0OOO0OO0O0000 =run_bash (O0O000000OO000OOO )#line:275
    if O00O0OOO0OO0O0000 !=0 :#line:276
        fun_email (f'{O00O0O000O0O0OOO0[-2]}/{O00O0O000O0O0OOO0[-1]}出错','datax error')#line:277
        raise SmartpipException ('datax error')#line:278
    if OOO0OO0OO00000000 :#line:279
        SmartpipException (_O0O00OO0OO00O0O0O (OOO0OO0OO00000000 .split (';'),O0OOO000O0000O00O ,db_connect ='hive',dev =dev ))#line:280
def readSqlFile (OO0O0O0OOO0OO000O ,para_dict =None ):#line:284
    if OO0O0O0OOO0OO000O .find ('.sql')<0 :#line:285
        return 'file type error'#line:286
    with open (OO0O0O0OOO0OO000O ,'r',encoding ='utf-8')as O00O000000OOOOOOO :#line:287
        OOO000000O00O0OO0 =O00O000000OOOOOOO .read ()#line:288
    OO00OO00O00OO0OO0 =readSqlstr (OOO000000O00O0OO0 ,para_dict )#line:289
    return OO00OO00O00OO0OO0 #line:290
def readSqoopFile (OO0OOO0O0OOO0OOOO ,para_dict =None ):#line:293
    if not OO0OOO0O0OOO0OOOO .endswith ('.sql'):#line:294
        return 'file type error'#line:295
    with open (OO0OOO0O0OOO0OOOO ,'r',encoding ='utf8')as O0000O000O0000O0O :#line:296
        O00000O0OO0OO000O =O0000O000O0000O0O .read ().strip ()#line:297
    OOO00OOO000O00O0O =re .match (r"/\*(.*?)\*/(.+)",O00000O0OO0OO000O ,re .M |re .S )#line:298
    OOOOO000OO00O0O0O =readSqlstr (OOO00OOO000O00O0O .group (1 ).strip (),para_dict )#line:299
    O0OO0OO00OO0OO000 =OOO00OOO000O00O0O .group (2 ).strip ()#line:300
    return OOOOO000OO00O0O0O ,O0OO0OO00OO0OO000 #line:301
def readSqlstr (OOO0OO0OO0O00OO00 ,para_dict =None ):#line:304
    OOOOOOOOOO00OOOO0 =re .sub (r"(\/\*(.|\n)*?\*\/)|--.*",'',OOO0OO0OO0O00OO00 .strip ())#line:305
    if para_dict :#line:306
        for O0OOO00O000O0O0OO ,O0OOOOO00OOOOO000 in para_dict .items ():#line:307
            if O0OOO00O000O0O0OO .isnumeric ():#line:308
                O0O0000O00O0OOO0O =get_dataset (O0OOOOO00OOOOO000 )#line:309
                print ('dataset:',O0O0000O00O0OOO0O )#line:310
                if O0O0000O00O0OOO0O['result'] != 'success':
                    raise SmartpipException(O0O0000O00O0OOO0O['data'])
                else:
                    O0O0000O00O0OOO0O = O0O0000O00O0OOO0O['data']
                if len (O0O0000O00O0OOO0O )>1 :#line:311
                    for O0000OO00OOOOOOO0 ,O000OO000OOO00OO0 in zip (O0O0000O00O0OOO0O [0 ],O0O0000O00O0OOO0O [1 ]):#line:312
                        OOOOOOOOOO00OOOO0 =OOOOOOOOOO00OOOO0 .replace ('$'+O0000OO00OOOOOOO0 ,str (O000OO000OOO00OO0 ))#line:313
            elif callable (O0OOOOO00OOOOO000 ):#line:314
                OOOO0OO0OOO0OO00O =O0OOOOO00OOOOO000 ()#line:315
                for O0000OO00OOOOOOO0 ,O000OO000OOO00OO0 in OOOO0OO0OOO0OO00O .items ():#line:316
                    OOOOOOOOOO00OOOO0 =OOOOOOOOOO00OOOO0 .replace ('$'+O0000OO00OOOOOOO0 ,str (O000OO000OOO00OO0 ))#line:317
            else :#line:318
                OOOOOOOOOO00OOOO0 =OOOOOOOOOO00OOOO0 .replace ('$'+O0OOO00O000O0O0OO ,str (O0OOOOO00OOOOO000 ))#line:319
    return OOOOOOOOOO00OOOO0 #line:320
def run_sql_file (OO0O0O00OOOOO0OO0 ,OO000000000O0O0O0 ,db_connect ='starrocks',para_dict =None ,dev =''):#line:323
    O0O0000O0OO00OOO0 =OO0O0O00OOOOO0OO0 .split ('/')#line:324
    try :#line:325
        OOOO0OO00OO0OOOO0 =readSqlFile (OO0O0O00OOOOO0OO0 ,para_dict ).split (';')#line:326
        OOO00O00OO0OOOOOO =OO000000000O0O0O0 .get (db_connect )#line:327
        if dev :#line:328
            if f'{db_connect}{dev}'in OO000000000O0O0O0 .keys ():#line:329
                OOO00O00OO0OOOOOO =OO000000000O0O0O0 .get (f'{db_connect}{dev}')#line:330
        OOOO0O00000O0O0O0 =connect_db_execute ().execute_sql_list (OOOO0OO00OO0OOOO0 ,db_connect ,connect_dict =OOO00O00OO0OOOOOO )#line:331
        return OOOO0O00000O0O0O0 #line:332
    except Exception as O00OO00O0000O0000 :#line:333
        fun_email ('{}/{}执行出错'.format (O0O0000O0OO00OOO0 [-2 ],O0O0000O0OO00OOO0 [-1 ]),str (O00OO00O0000O0000 .args ))#line:334
        raise SmartpipException (str (O00OO00O0000O0000 .args ))#line:335
def _O0O00OO0OO00O0O0O (O00OOOO0000000OO0 ,OOO0000OOO00000OO ,db_connect ='starrocks',para_dict =None ,dev =''):#line:338
    try :#line:339
        if isinstance (O00OOOO0000000OO0 ,str ):#line:340
            O00OOOO0000000OO0 =readSqlstr (O00OOOO0000000OO0 ,para_dict ).split (';')#line:341
        O0OOO0OO0O0O00OOO =OOO0000OOO00000OO .get (db_connect )#line:342
        if dev :#line:343
            if f'{db_connect}{dev}'in OOO0000OOO00000OO .keys ():#line:344
                O0OOO0OO0O0O00OOO =OOO0000OOO00000OO .get (f'{db_connect}{dev}')#line:345
        O00O00O00OOOOOOOO =connect_db_execute ().execute_sql_list (O00OOOO0000000OO0 ,db_connect ,connect_dict =O0OOO0OO0O0O00OOO )#line:346
        return O00O00O00OOOOOOOO #line:347
    except Exception as O0O00000O00O0OOOO :#line:348
        fun_email ('SQL执行出错',f'{O00OOOO0000000OO0}{O0O00000O00O0OOOO.args}')#line:349
        raise SmartpipException (str (O0O00000O00O0OOOO .args ))#line:350
def run_sp (OO0000O0O0O000O0O ,OO0000O000O00OO00 ,db_connect ='oracle',sp_para =None ,dev =''):#line:353
    try :#line:354
        OO0OO00O0OO0O0O00 =OO0000O000O00OO00 .get (db_connect )#line:355
        if dev :#line:356
            if f'{db_connect}{dev}'in OO0000O000O00OO00 .keys ():#line:357
                OO0OO00O0OO0O0O00 =OO0000O000O00OO00 .get (f'{db_connect}{dev}')#line:358
        connect_db_execute ().excute_proc (OO0000O0O0O000O0O ,OO0OO00O0OO0O0O00 ,sp_para )#line:359
    except Exception as O0OOOOOOOOO0O0OOO :#line:360
        fun_email ('{}执行出错'.format (OO0000O0O0O000O0O ),str (O0OOOOOOOOO0O0OOO .args ))#line:361
        raise SmartpipException (str (O0OOOOOOOOO0O0OOO .args ))#line:362
def run_kettle (OO000OOO0O00OO0O0 ,para_str ='',dev =False ):#line:366
    ""#line:373
    O0O0O0OOO0000OOO0 =OO000OOO0O00OO0O0 .split ('/')#line:374
    print ('kettle job start')#line:375
    if '.ktr'in OO000OOO0O00OO0O0 :#line:377
        OO0O000OOO00OO0O0 =f'{KETTLE_HOME}/pan.sh -level=Basic -file={OO000OOO0O00OO0O0}{para_str}'#line:378
    else :#line:379
        OO0O000OOO00OO0O0 =f'{KETTLE_HOME}/kitchen.sh -level=Basic -file={OO000OOO0O00OO0O0}{para_str}'#line:380
    print (OO0O000OOO00OO0O0 )#line:381
    O0OO0O0O0OOOOOOOO ,O000OOO00O00OO0O0 =run_bash (OO0O000OOO00OO0O0 )#line:385
    if O000OOO00O00OO0O0 ==0 :#line:386
        print ('{} 完成数据抽取'.format (str (OO000OOO0O00OO0O0 )))#line:387
    else :#line:388
        print ('{} 执行错误'.format (OO000OOO0O00OO0O0 ))#line:389
        fun_email ('{}/{}出错'.format (O0O0O0OOO0000OOO0 [-2 ],O0O0O0OOO0000OOO0 [-1 ]),str (O0OO0O0O0OOOOOOOO ))#line:390
        raise SmartpipException ('Run Kettle Error')#line:391
def hdfsStarrocks (OOO0O0000OOO0000O ,OO0O00OOOO0OO0O00 ,para_dict =None ):#line:395
    ""#line:399
    O000OOOOO0O0O00O0 =OOO0O0000OOO0000O .split ('/')#line:400
    print ('starrocks load job start')#line:401
    O0O0OO0O00O0OOOO0 ,O00OO0OOO0OOO0O0O =readSqoopFile (OOO0O0000OOO0000O ,para_dict =para_dict )#line:402
    O0O0OO0O00O0OOOO0 =O0O0OO0O00O0OOOO0 .split ('\n')#line:403
    OOOOO0OO0000OO000 ={'LABEL':f'{O000OOOOO0O0O00O0[-2]}{O000OOOOO0O0O00O0[-1][:-4]}{int(time.time())}','HDFS':HIVE_HOME }#line:404
    for O0O00O00000O0OO0O in O0O0OO0O00O0OOOO0 :#line:405
        OOOO0OO00OO0OO00O =O0O00O00000O0OO0O .find ('=')#line:406
        if OOOO0OO00OO0OO00O >0 :#line:407
            OOOOO0OO0000OO000 [O0O00O00000O0OO0O [:OOOO0OO00OO0OO00O ].strip ()]=O0O00O00000O0OO0O [OOOO0OO00OO0OO00O +1 :].strip ()#line:408
    O0O00OO000OO000OO =OOOOO0OO0000OO000 .get ('sleepTime')#line:410
    if O0O00OO000OO000OO :#line:411
        O0O00OO000OO000OO =int (O0O00OO000OO000OO )#line:412
        if O0O00OO000OO000OO <30 :#line:413
            O0O00OO000OO000OO =30 #line:414
    else :#line:415
        O0O00OO000OO000OO =30 #line:416
    O000OOOO00O00O0O0 =OOOOO0OO0000OO000 .get ('maxTime')#line:418
    if O000OOOO00O00O0O0 :#line:419
        O000OOOO00O00O0O0 =int (O000OOOO00O00O0O0 )#line:420
        if O000OOOO00O00O0O0 >3600 :#line:421
            O000OOOO00O00O0O0 =3600 #line:422
    else :#line:423
        O000OOOO00O00O0O0 =600 #line:424
    _O0O00OO0OO00O0O0O (O00OO0OOO0OOO0O0O ,OO0O00OOOO0OO0O00 ,db_connect ='starrocks',para_dict =OOOOO0OO0000OO000 )#line:426
    time .sleep (O0O00OO000OO000OO )#line:427
    O00OOO0OO000O000O =f'''show load from {OOOOO0OO0000OO000.get('targetDB')} where label = '{OOOOO0OO0000OO000['LABEL']}' order by CreateTime desc limit 1 '''#line:428
    OO0OOO0O0O0O00000 ='start to check label'#line:429
    try :#line:430
        while True :#line:431
            OO0OOO0O0O0O00000 =_O0O00OO0OO00O0O0O ([O00OOO0OO000O000O ],OO0O00OOOO0OO0O00 ,db_connect ='starrocks')#line:432
            print (OO0OOO0O0O0O00000 )#line:433
            OO00O0OO0O0O0OOO0 =OO0OOO0O0O0O00000 [1 ][2 ]#line:434
            if OO00O0OO0O0O0OOO0 =='CANCELLED':#line:435
                raise Exception (f'Starrocks:{OO00O0OO0O0O0OOO0}')#line:436
            elif OO00O0OO0O0O0OOO0 =='FINISHED':#line:437
                print ('Load completed')#line:438
                break #line:439
            if O000OOOO00O00O0O0 <=0 :#line:440
                raise Exception ('超时未完成')#line:441
            else :#line:442
                time .sleep (O0O00OO000OO000OO )#line:443
                O000OOOO00O00O0O0 =O000OOOO00O00O0O0 -O0O00OO000OO000OO #line:444
    except Exception as O0OO00O00OO00O0OO :#line:445
        print ('{} 执行错误'.format (OOO0O0000OOO0000O ))#line:446
        fun_email ('{}/{}执行出错'.format (O000OOOOO0O0O00O0 [-2 ],O000OOOOO0O0O00O0 [-1 ]),str (OO0OOO0O0O0O00000 ))#line:447
        raise SmartpipException (str (O0OO00O00OO00O0OO .args ))#line:448
def kafkaStarrocks (O000OOO0O0OOOOO00 ,O0O00O0O0O0O0OO0O ,OO0O00000O0O000OO ,O0OOO0O000OOOO000 ,O00OO00O0000O0OO0 ,dev =''):#line:451
    with open (O000OOO0O0OOOOO00 ,'r',encoding ='utf8')as OO0O0OO0000OO0O00 :#line:452
        OO0O00O0000000000 =readSqlstr (OO0O0OO0000OO0O00 .read ().strip (),para_dict =O00OO00O0000O0OO0 )#line:453
    OO0O00O0000000000 =OO0O00O0000000000 .split ('##')#line:454
    O0OO000000000OO00 ={}#line:455
    for OOO00OO000O00O00O in OO0O00O0000000000 :#line:456
        O0OO0OO0OO0OO0O0O =OOO00OO000O00O00O .find ('=')#line:457
        if O0OO0OO0OO0OO0O0O >0 :#line:458
            OO000000O0OOO0OOO =OOO00OO000O00O00O [O0OO0OO0OO0OO0O0O +1 :].replace ('\n',' ').strip ()#line:459
            if OO000000O0OOO0OOO :#line:460
                O0OO000000000OO00 [OOO00OO000O00O00O [:O0OO0OO0OO0OO0O0O ].strip ()]=OO000000O0OOO0OOO #line:461
    O00OO0O000O00OO00 =O0OO000000000OO00 .pop ('topic')#line:462
    OO0OOO00O0O0O000O =O0OO000000000OO00 .pop ('table')#line:463
    OOOOOO0OO000O000O =O0OO000000000OO00 .keys ()#line:464
    if 'skipError'in OOOOOO0OO000O000O :#line:465
        skipError =O0OO000000000OO00 .pop ('skipError')#line:466
    else :#line:467
        skipError =None #line:468
    if 'kafkaConn'in OOOOOO0OO000O000O :#line:469
        O0O0000O0OOOOO0O0 =O0OO000000000OO00 .pop ('kafkaConn')#line:470
    else :#line:471
        O0O0000O0OOOOO0O0 ='default'#line:472
    if 'offsets'in OOOOOO0OO000O000O :#line:473
        O0O0O00OOO00OO0O0 =json .loads (O0OO000000000OO00 .pop ('offsets'))#line:474
    else :#line:475
        O0O0O00OOO00OO0O0 =None #line:476
    if 'json_root'in OOOOOO0OO000O000O :#line:477
        O0O0OOO00OO0OO000 =O0OO000000000OO00 .pop ('json_root')#line:478
    else :#line:479
        O0O0OOO00OO0OO000 =None #line:480
    if 'jsonpaths'in OOOOOO0OO000O000O :#line:481
        O00000OO0000OOOO0 =O0OO000000000OO00 .get ('jsonpaths')#line:482
        if not O00000OO0000OOOO0 .startswith ('['):#line:483
            O00000OO0000OOOO0 =O00000OO0000OOOO0 .split (',')#line:484
            O00000OO0000OOOO0 =json .dumps (['$.'+O000OOOO0OO00OOOO .strip ()for O000OOOO0OO00OOOO in O00000OO0000OOOO0 ])#line:485
            O0OO000000000OO00 ['jsonpaths']=O00000OO0000OOOO0 #line:486
    OO0OOOO00OOOOO0OO =_O00OO000O0O0OO000 (O00OO0O000O00OO00 ,O0O00O0O0O0O0OO0O [O0O0000O0OOOOO0O0 ],O0OOO0O000OOOO000 ,O0O0O00OOO00OO0O0 )#line:487
    def O0O0OO0O00OO0OOO0 (OO0OO0O00O0O00O0O ):#line:489
        OO00000O00OO00OO0 =b''#line:490
        OOO000OO0O0O00O00 =None #line:491
        if 'format'in OOOOOO0OO000O000O :#line:492
            for OOO000OO0O0O00O00 in OO0OO0O00O0O00O0O :#line:493
                O00OO000O0O00O0OO =OOO000OO0O0O00O00 .value #line:494
                if O0O0OOO00OO0OO000 :#line:495
                    O00OO000O0O00O0OO =json .loads (O00OO000O0O00O0OO .decode ('utf8'))#line:496
                    O00OO000O0O00O0OO =json .dumps (O00OO000O0O00O0OO [O0O0OOO00OO0OO000 ]).encode ('utf8')#line:497
                if O00OO000O0O00O0OO .startswith (b'['):#line:498
                    OO00000O00OO00OO0 =OO00000O00OO00OO0 +b','+O00OO000O0O00O0OO [1 :-1 ]#line:499
                else :#line:500
                    OO00000O00OO00OO0 =OO00000O00OO00OO0 +b','+O00OO000O0O00O0OO #line:501
                if len (OO00000O00OO00OO0 )>94857600 :#line:502
                    streamStarrocks (OO0OOO00O0O0O000O ,OO0O00000O0O000OO ,O0OO000000000OO00 ,OO00000O00OO00OO0 ,skipError )#line:503
                    OO0OOOO00OOOOO0OO .write_offset (OOO000OO0O0O00O00 .partition ,OOO000OO0O0O00O00 .offset +1 )#line:504
                    OO00000O00OO00OO0 =b''#line:505
                if OOO000OO0O0O00O00 .offset ==OO0OOOO00OOOOO0OO .end_offset -1 :#line:506
                    break #line:507
        else :#line:508
            for OOO000OO0O0O00O00 in OO0OO0O00O0O00O0O :#line:509
                O00OO000O0O00O0OO =OOO000OO0O0O00O00 .value #line:510
                if O0O0OOO00OO0OO000 :#line:511
                    O00OO000O0O00O0OO =json .loads (O00OO000O0O00O0OO .decode ('utf8'))#line:512
                    O00OO000O0O00O0OO =json .dumps (O00OO000O0O00O0OO [O0O0OOO00OO0OO000 ]).encode ('utf8')#line:513
                OO00000O00OO00OO0 =OO00000O00OO00OO0 +b'\n'+O00OO000O0O00O0OO #line:514
                if len (OO00000O00OO00OO0 )>94857600 :#line:515
                    streamStarrocks (OO0OOO00O0O0O000O ,OO0O00000O0O000OO ,O0OO000000000OO00 ,OO00000O00OO00OO0 ,skipError )#line:516
                    OO0OOOO00OOOOO0OO .write_offset (OOO000OO0O0O00O00 .partition ,OOO000OO0O0O00O00 .offset +1 )#line:517
                    OO00000O00OO00OO0 =b''#line:518
                if OOO000OO0O0O00O00 .offset ==OO0OOOO00OOOOO0OO .end_offset -1 :#line:519
                    break #line:520
        print (OO00000O00OO00OO0 [1 :1000 ])#line:521
        if OO00000O00OO00OO0 :#line:522
            streamStarrocks (OO0OOO00O0O0O000O ,OO0O00000O0O000OO ,O0OO000000000OO00 ,OO00000O00OO00OO0 ,skipError )#line:523
        return OOO000OO0O0O00O00 #line:524
    OO0OOOO00OOOOO0OO .consumer_topic (O0O0OO0O00OO0OOO0 )#line:526
def apiStarrocks (OOO00OO0OO00OO0OO ,O00O000OOO0O0000O ,OOOO0OO00O0O00OO0 ,O0O00O0OOOOO0OOO0 ):#line:529
    with open (OOO00OO0OO00OO0OO ,'r',encoding ='utf8')as O00000O0O0OOO0OOO :#line:530
        O000O0OO0O0OO00OO =readSqlstr (O00000O0O0OOO0OOO .read ().strip (),para_dict =O0O00O0OOOOO0OOO0 )#line:531
    O000O0OO0O0OO00OO =O000O0OO0O0OO00OO .split ('##')#line:532
    O0OO0000O00OO000O ={}#line:533
    for OO00O0OOOOOOOO0OO in O000O0OO0O0OO00OO :#line:534
        O0O00OOO0O0O00000 =OO00O0OOOOOOOO0OO .find ('=')#line:535
        if O0O00OOO0O0O00000 >0 :#line:536
            O000O000OOO0OO0O0 =OO00O0OOOOOOOO0OO [O0O00OOO0O0O00000 +1 :].replace ('\n',' ').strip ()#line:537
            if O000O000OOO0OO0O0 :#line:538
                O0OO0000O00OO000O [OO00O0OOOOOOOO0OO [:O0O00OOO0O0O00000 ].strip ()]=O000O000OOO0OO0O0 #line:539
    OO0O0O0OOO0000O00 =O0OO0000O00OO000O .pop ('table')#line:540
    O0O0OO000O0O0O0OO =O0OO0000O00OO000O .keys ()#line:541
    if 'param'in O0O0OO000O0O0O0OO :#line:542
        O0O0OO0OO0O0O000O =O0OO0000O00OO000O .pop ('param')#line:543
    else :#line:544
        O0O0OO0OO0O0O000O =None #line:545
    if 'apiConn'in O0O0OO000O0O0O0OO :#line:546
        OO0OOOOO00OOOOOOO =O0OO0000O00OO000O .pop ('apiConn')#line:547
    else :#line:548
        OO0OOOOO00OOOOOOO ='default'#line:549
    if 'skipError'in O0O0OO000O0O0O0OO :#line:550
        skipError =O0OO0000O00OO000O .pop ('skipError')#line:551
    else :#line:552
        skipError =None #line:553
    if 'jsonpaths'in O0O0OO000O0O0O0OO :#line:554
        OO0O000O0O0000OOO =O0OO0000O00OO000O .get ('jsonpaths')#line:555
        if not OO0O000O0O0000OOO .startswith ('['):#line:556
            OO0O000O0O0000OOO =OO0O000O0O0000OOO .split (',')#line:557
            OO0O000O0O0000OOO =json .dumps (['$.'+OOOOOO0000OOOO00O .strip ()for OOOOOO0000OOOO00O in OO0O000O0O0000OOO ])#line:558
            O0OO0000O00OO000O ['jsonpaths']=OO0O000O0O0000OOO #line:559
    OO0O000O0O0OO000O =O00O000OOO0O0000O [OO0OOOOO00OOOOOOO ](O0O0OO0OO0O0O000O )#line:560
    if OO0O000O0O0OO000O :#line:561
        streamStarrocks (OO0O0O0OOO0000O00 ,OOOO0OO00O0O00OO0 ,O0OO0000O00OO000O ,OO0O000O0O0OO000O ,skipError )#line:562
    else :#line:563
        print ('无数据')#line:564
def streamStarrocks (OO000O0OO0OO0000O ,OO0OOO00OO00O0000 ,OOO000OO0000O0000 ,O00OO00O0000O000O ,skipError =False ):#line:567
    ""#line:570
    import base64 ,uuid #line:571
    O00O0O0OO0OO00OOO ,OO000O0OO0OO0000O =OO000O0OO0OO0000O .split ('.')#line:572
    O0OO00OOO0O000OO0 =str (base64 .b64encode (f'{OO0OOO00OO00O0000["user"]}:{OO0OOO00OO00O0000["password"]}'.encode ('utf-8')),'utf-8')#line:573
    O00OO00O0000O000O =O00OO00O0000O000O .strip ()#line:574
    if O00OO00O0000O000O .startswith (b','):#line:575
        OOO000OO0000O0000 ['strip_outer_array']='true'#line:576
        O00OO00O0000O000O =b'['+O00OO00O0000O000O [1 :]+b']'#line:577
    OO0000OOO0OO00000 ={'Content-Type':'application/json','Authorization':f'Basic {O0OO00OOO0O000OO0}','label':f'{OO000O0OO0OO0000O}{uuid.uuid4()}',**OOO000OO0000O0000 }#line:583
    OO00O0O0OO0O00O00 =f"{OO0OOO00OO00O0000['url']}/api/{O00O0O0OO0OO00OOO}/{OO000O0OO0OO0000O}/_stream_load"#line:584
    print ('start loading to starrocks....')#line:585
    O0OO0OOO000OOO000 =requests .put (OO00O0O0OO0O00O00 ,headers =OO0000OOO0OO00000 ,data =O00OO00O0000O000O ).json ()#line:586
    print (O0OO0OOO000OOO000 )#line:587
    if O0OO0OOO000OOO000 ['Status']=='Fail':#line:588
        if skipError :#line:589
            print (f'Starrocks Load Error, Skip this offset')#line:590
        else :#line:591
            raise SmartpipException ('Starrocks Load Error')#line:592
def routineStarrocks (O00000000O000OO0O ,OO000000OO0O0O0OO ,flag =''):#line:595
    O0O000OOOO00000OO =_O0O00OO0OO00O0O0O ([f'SHOW ROUTINE LOAD FOR {OO000000OO0O0O0OO}'],O00000000O000OO0O ,db_connect ='starrocks')#line:596
    O0O000OOOO00000OO =dict (zip (O0O000OOOO00000OO [0 ],O0O000OOOO00000OO [1 ]))#line:597
    print ('状态:',O0O000OOOO00000OO ['State'])#line:598
    print ('统计:',O0O000OOOO00000OO ['Statistic'])#line:599
    print ('进度:',O0O000OOOO00000OO ['Progress'])#line:600
    if O0O000OOOO00000OO ['State']!='RUNNING':#line:601
        print ('ERROR: ',O0O000OOOO00000OO ['ReasonOfStateChanged'])#line:602
        if not flag :#line:603
            raise SmartpipException ('Starrocks Routine Load fail')#line:604
from airflow .utils .session import provide_session #line:610
@provide_session #line:613
def point_test (OOO0000O0O000OO00 ,sleeptime ='',maxtime ='',session =None ):#line:614
    ""#line:621
    if sleeptime :#line:622
        sleeptime =int (sleeptime )#line:623
        sleeptime =sleeptime if sleeptime >60 else 60 #line:624
    if maxtime :#line:625
        maxtime =int (maxtime )#line:626
        maxtime =maxtime if maxtime <60 *60 *2 else 60 *60 *2 #line:627
    else :#line:628
        maxtime =0 #line:629
    try :#line:630
        O000000OOO0OOOOOO =f"select start_date,state from dag_run where dag_id ='{OOO0000O0O000OO00}' ORDER BY id desc LIMIT 1"#line:631
        while True :#line:632
            O0O0OO0OOOO00O000 =session .execute (O000000OOO0OOOOOO ).fetchall ()#line:633
            if O0O0OO0OOOO00O000 [0 ][1 ]!='success':#line:634
                if maxtime >0 and O0O0OO0OOOO00O000 [0 ][1 ]!='failed':#line:635
                    print ('waiting...'+O0O0OO0OOOO00O000 [0 ][1 ])#line:636
                    time .sleep (sleeptime )#line:637
                    maxtime =maxtime -sleeptime #line:638
                else :#line:639
                    OO000OOOO00000000 =O0O0OO0OOOO00O000 [0 ][0 ].strftime ("%Y-%m-%d %H:%M:%S")#line:640
                    O0OOO00O0OO0O0OO0 ='所依赖的dag:'+OOO0000O0O000OO00 +',状态为'+O0O0OO0OOOO00O000 [0 ][1 ]+'.其最新的执行时间为'+OO000OOOO00000000 #line:641
                    fun_email (O0OOO00O0OO0O0OO0 ,'前置DAG任务未成功')#line:642
                    raise SmartpipException (O0OOO00O0OO0O0OO0 )#line:643
            else :#line:644
                print ('success...',O0O0OO0OOOO00O000 )#line:645
                break #line:646
    except Exception as OO0OOOO0OO00OOO0O :#line:647
        raise SmartpipException (str (OO0OOOO0OO00OOO0O .args ))#line:648
class connect_db_execute ():#line:653
    def __init__ (O0OO00O0O0O0O00OO ,dev =False ,db =''):#line:654
        O0OO00O0O0O0O00OO .dev =dev #line:655
    def insert_contents (O00OO00OO0OOOOO0O ,O000OO000O0O0O00O ,O0OOOOOOOO00OOOOO ,per_in =1000 ,connect_dict =None ):#line:657
        OOO0000OOO000OO00 =time .time ()#line:658
        logging .info ('starting to execute insert contents...')#line:659
        if isinstance (connect_dict ,dict ):#line:660
            OOOOO00O00OOO000O =connect_dict ['dbtype']#line:661
        else :#line:662
            if connect_dict =='':#line:663
                OOOOO00O00OOO000O ='oracle'#line:664
            else :#line:665
                OOOOO00O00OOO000O =connect_dict #line:666
            connect_dict =None #line:667
        O0O0O00OO00OOO0O0 =getattr (O00OO00OO0OOOOO0O ,'insert_contents_'+OOOOO00O00OOO000O )#line:668
        O000000O00OOO0OO0 =O0O0O00OO00OOO0O0 (O000OO000O0O0O00O ,O0OOOOOOOO00OOOOO ,per_in ,connect_dict )#line:669
        logging .info ('execute insert contents time : {}ms'.format (time .time ()-OOO0000OOO000OO00 ))#line:670
        return O000000O00OOO0OO0 #line:671
    def impala (OOOO000O00OOO000O ,O0OO00O0OO0O00000 ,connect_dict =None ):#line:673
        ""#line:674
        from impala .dbapi import connect as impala #line:675
        O0O0OOOO0000OOOO0 =impala (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =int (connect_dict ['port']),auth_mechanism ='PLAIN')#line:682
        OOO00O0O00OO0O00O =O0O0OOOO0000OOOO0 .cursor ()#line:683
        OO00O000OOO0000OO =r'^insert\s|^update\s|^truncate\s|^delete\s|^load\s|^refresh\s|^upsert\s'#line:684
        OO0000OO0O0OOO000 =None #line:685
        for OOO0OO0000O0OO000 in O0OO00O0OO0O00000 :#line:686
            print (OOO0OO0000O0OO000 )#line:687
            OOO0OO0000O0OO000 =OOO0OO0000O0OO000 .strip ()#line:688
            if not OOO0OO0000O0OO000 :#line:689
                continue #line:690
            if re .search (OO00O000OOO0000OO ,OOO0OO0000O0OO000 ,re .I |re .IGNORECASE ):#line:691
                OOO00O0O00OO0O00O .execute (OOO0OO0000O0OO000 )#line:692
            else :#line:693
                OOO00O0O00OO0O00O .execute (OOO0OO0000O0OO000 )#line:694
                try :#line:695
                    OO0000OO0O0OOO000 =OOO00O0O00OO0O00O .fetchall ()#line:696
                except Exception as OOOO000OO00O000OO :#line:697
                    print (OOOO000OO00O000OO .args )#line:698
        O0O0OOOO0000OOOO0 .close ()#line:699
        return OO0000OO0O0OOO000 #line:700
    def hive (O00OO00OOO0O00O0O ,OO0O0OOOOO000000O ,connect_dict =None ):#line:702
        ""#line:703
        from impala .dbapi import connect as impala #line:704
        OOO000O0OOO0O00O0 =impala (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =int (connect_dict ['port']),auth_mechanism ='PLAIN')#line:711
        O0O000O0OOO0OOO00 =OOO000O0OOO0O00O0 .cursor ()#line:712
        O00O0O00O000000OO =r'^insert\s|^update\s|^truncate\s|^delete\s|^load\s'#line:713
        OO00O00O000000O00 =None #line:714
        for OOOO00O0O0O00OO00 in OO0O0OOOOO000000O :#line:715
            OOOO00O0O0O00OO00 =OOOO00O0O0O00OO00 .strip ()#line:716
            if not OOOO00O0O0O00OO00 :#line:717
                continue #line:718
            print (OOOO00O0O0O00OO00 )#line:719
            if OOOO00O0O0O00OO00 .startswith ('refresh'):#line:720
                connect_dict ['port']=21050 #line:721
                O00OO00OOO0O00O0O .impala ([OOOO00O0O0O00OO00 ],connect_dict =connect_dict )#line:722
            else :#line:723
                if re .search (O00O0O00O000000OO ,OOOO00O0O0O00OO00 ,re .I |re .IGNORECASE ):#line:724
                    O0O000O0OOO0OOO00 .execute (OOOO00O0O0O00OO00 )#line:725
                else :#line:726
                    O0O000O0OOO0OOO00 .execute (OOOO00O0O0O00OO00 )#line:727
                    try :#line:728
                        OO00O00O000000O00 =O0O000O0OOO0OOO00 .fetchall ()#line:729
                    except Exception as O000000O000O0OOO0 :#line:730
                        print (O000000O000O0OOO0 .args )#line:731
        OOO000O0OOO0O00O0 .close ()#line:732
        return OO00O00O000000O00 #line:733
    def mysql (OO00OO00000OOO00O ,O0OOO0OO0OOO0OO0O ,connect_dict =None ):#line:735
        import pymysql #line:736
        OO000OO0OO0O000O0 =pymysql .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =connect_dict ['port'],database =connect_dict ['db'])#line:743
        try :#line:744
            OOOO0O0O0O000000O =OO000OO0OO0O000O0 .cursor ()#line:745
            OO00000OO00O0O0OO =r'^insert\s|^update\s|^truncate\s|^delete\s|^load\s'#line:746
            for O0OOOO000O0OOOOOO in O0OOO0OO0OOO0OO0O :#line:747
                O0OOOO000O0OOOOOO =O0OOOO000O0OOOOOO .strip ()#line:748
                if not O0OOOO000O0OOOOOO :#line:749
                    continue #line:750
                print (O0OOOO000O0OOOOOO )#line:751
                if re .search (OO00000OO00O0O0OO ,O0OOOO000O0OOOOOO ,re .I |re .IGNORECASE ):#line:752
                    try :#line:753
                        OOOO0O0O0O000000O .execute (O0OOOO000O0OOOOOO )#line:754
                        OO000OO0OO0O000O0 .commit ()#line:755
                    except Exception as OO0000OOOOOO0O00O :#line:756
                        OO000OO0OO0O000O0 .rollback ()#line:757
                        raise OO0000OOOOOO0O00O #line:758
                else :#line:759
                    OOOO0O0O0O000000O .execute (O0OOOO000O0OOOOOO )#line:760
                    O000OOOO0O00OOO00 =OOOO0O0O0O000000O .fetchall ()#line:761
                    O000OOOO0O00OOO00 =[[OOOO00OOOO000O00O [0 ]for OOOO00OOOO000O00O in OOOO0O0O0O000000O .description ]]+list (O000OOOO0O00OOO00 )#line:762
                    return O000OOOO0O00OOO00 #line:763
        except Exception as O0O0OOOOO00000O00 :#line:764
            raise O0O0OOOOO00000O00 #line:765
        finally :#line:766
            OO000OO0OO0O000O0 .close ()#line:767
    def starrocks (OOOOOO0OO0OO0O0OO ,OO00OO000OO000O0O ,connect_dict =None ):#line:769
        return OOOOOO0OO0OO0O0OO .mysql (OO00OO000OO000O0O ,connect_dict )#line:770
    def oracle (O00O0O0OOO0O00OOO ,OOOOOO0O00O0OOO0O ,connect_dict =None ):#line:772
        import cx_Oracle #line:773
        OO0000O00OOO00000 ='{}/{}@{}/{}'.format (connect_dict ['user'],connect_dict ['password'],connect_dict ['host'],connect_dict ['db'])#line:778
        O00O00O0O0O0O0OO0 =cx_Oracle .connect (OO0000O00OOO00000 )#line:779
        try :#line:780
            OO000000O0OO0OOO0 =O00O00O0O0O0O0OO0 .cursor ()#line:781
            OOOO000O0000OOO0O =r'^insert\s|^update\s|^truncate\s|^delete\s|^comment\s'#line:782
            for O0O0OO0OOO0OOOOO0 in OOOOOO0O00O0OOO0O :#line:783
                O0O0OO0OOO0OOOOO0 =O0O0OO0OOO0OOOOO0 .strip ()#line:784
                if not O0O0OO0OOO0OOOOO0 :#line:785
                    continue #line:786
                if re .search (OOOO000O0000OOO0O ,O0O0OO0OOO0OOOOO0 ,re .I ):#line:787
                    try :#line:788
                        OO000000O0OO0OOO0 .execute (O0O0OO0OOO0OOOOO0 )#line:789
                        O00O00O0O0O0O0OO0 .commit ()#line:790
                    except Exception as OOOOOOOO0OOO0O00O :#line:791
                        if O0O0OO0OOO0OOOOO0 .startswith ('comment'):#line:792
                            print ('err:',O0O0OO0OOO0OOOOO0 )#line:793
                            continue #line:794
                        O00O00O0O0O0O0OO0 .rollback ()#line:795
                        raise OOOOOOOO0OOO0O00O #line:796
                else :#line:797
                    OO000000O0OO0OOO0 .execute (O0O0OO0OOO0OOOOO0 )#line:798
                    OOO0OOOO0O000OOOO =OO000000O0OO0OOO0 .fetchall ()#line:799
                    OOO0OOOO0O000OOOO =[[O0OOO000OOO00OOO0 [0 ]for O0OOO000OOO00OOO0 in OO000000O0OO0OOO0 .description ]]+list (OOO0OOOO0O000OOOO )#line:800
                    return OOO0OOOO0O000OOOO #line:801
        except Exception as OO000O0O000OOOOO0 :#line:802
            raise OO000O0O000OOOOO0 #line:803
        finally :#line:804
            O00O00O0O0O0O0OO0 .close ()#line:805
    def gp (O0OO0OO000OO000O0 ,O0O00OOOO00OO000O ,connect_dict =None ):#line:807
        import psycopg2 #line:808
        O0OO000O0000OO0O0 =psycopg2 .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =connect_dict ['port'],database =connect_dict ['db'])#line:815
        try :#line:816
            O000O0O0OOOOOO00O =O0OO000O0000OO0O0 .cursor ()#line:817
            OOOOOO0OO00OOOO00 =r'^insert\s|^update\s|^truncate\s|^delete\s'#line:818
            for O00OO00OOOOOOOOO0 in O0O00OOOO00OO000O :#line:819
                O00OO00OOOOOOOOO0 =O00OO00OOOOOOOOO0 .strip ()#line:820
                if not O00OO00OOOOOOOOO0 :#line:821
                    continue #line:822
                if re .search (OOOOOO0OO00OOOO00 ,O00OO00OOOOOOOOO0 ,re .I |re .IGNORECASE ):#line:823
                    try :#line:824
                        O000O0O0OOOOOO00O .execute (O00OO00OOOOOOOOO0 )#line:825
                        O0OO000O0000OO0O0 .commit ()#line:826
                    except Exception as O0OOOO0O000O0O000 :#line:827
                        O0OO000O0000OO0O0 .rollback ()#line:828
                        raise O0OOOO0O000O0O000 #line:829
                else :#line:830
                    O000O0O0OOOOOO00O .execute (O00OO00OOOOOOOOO0 )#line:831
                    OOO00OO0O00O0O0O0 =O000O0O0OOOOOO00O .fetchall ()#line:832
                    OOO00OO0O00O0O0O0 =[[OO00O0O0OOO0OO0O0 [0 ]for OO00O0O0OOO0OO0O0 in O000O0O0OOOOOO00O .description ]]+list (OOO00OO0O00O0O0O0 )#line:833
                    return OOO00OO0O00O0O0O0 #line:834
        except Exception as OO0O0OO00OOOOO0OO :#line:835
            raise OO0O0OO00OOOOO0OO #line:836
        finally :#line:837
            O0OO000O0000OO0O0 .close ()#line:838
    def mssql (O00O0OOOO00OO0O00 ,OOO0OO0OO00OO0OOO ,connect_dict =None ):#line:840
        import pymssql #line:841
        if connect_dict ['port']:#line:842
            O00OOOO000000OOOO =pymssql .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],port =int (connect_dict ['port']),database =connect_dict ['db'],charset ="utf8",)#line:850
        else :#line:851
            O00OOOO000000OOOO =pymssql .connect (user =connect_dict ['user'],password =connect_dict ['password'],host =connect_dict ['host'],database =connect_dict ['db'],charset ="utf8",)#line:858
        try :#line:859
            O0O0O0OO0O0O00O0O =O00OOOO000000OOOO .cursor ()#line:860
            O00000OO00OO0000O =r'^insert\s|^update\s|^truncate\s|^delete\s'#line:861
            for O0OO00OO0O000O0O0 in OOO0OO0OO00OO0OOO :#line:862
                O0OO00OO0O000O0O0 =O0OO00OO0O000O0O0 .strip ()#line:863
                if not O0OO00OO0O000O0O0 :#line:864
                    continue #line:865
                if re .search (O00000OO00OO0000O ,O0OO00OO0O000O0O0 ,re .I |re .IGNORECASE ):#line:866
                    try :#line:867
                        O0O0O0OO0O0O00O0O .execute (O0OO00OO0O000O0O0 )#line:868
                        O00OOOO000000OOOO .commit ()#line:869
                    except Exception as O00O0O00O000O0000 :#line:870
                        O00OOOO000000OOOO .rollback ()#line:871
                        raise O00O0O00O000O0000 #line:872
                else :#line:873
                    O0O0O0OO0O0O00O0O .execute (O0OO00OO0O000O0O0 )#line:874
                    O0OO0OOOOO000O0O0 =O0O0O0OO0O0O00O0O .fetchall ()#line:875
                    O0OO0OOOOO000O0O0 =[[O00OOO00000000000 [0 ]for O00OOO00000000000 in O0O0O0OO0O0O00O0O .description ]]+list (O0OO0OOOOO000O0O0 )#line:876
                    return O0OO0OOOOO000O0O0 #line:877
        except Exception as OOOOOOOO0OOOOOOO0 :#line:878
            raise OOOOOOOO0OOOOOOO0 #line:879
        finally :#line:880
            O00OOOO000000OOOO .close ()#line:881
    def execute_sql_list (O0OO00000O000OO0O ,O00OOO0000000O00O ,db_connect ='',connect_dict =None ):#line:883
        if db_connect =='':db_connect ='oracle'#line:884
        O0O000O00O0OOO0OO =getattr (O0OO00000O000OO0O ,db_connect )#line:885
        return O0O000O00O0OOO0OO (O00OOO0000000O00O ,connect_dict =connect_dict )#line:886
    def excute_proc (OOOOOOOO00O00OO00 ,O00O0OO00O0O00OOO ,OOOO0O0OOO00O0O0O ,proc_para =None ):#line:888
        import cx_Oracle #line:889
        O00OOO00OOO00O00O ='{}/{}@{}/{}'.format (OOOO0O0OOO00O0O0O ['user'],OOOO0O0OOO00O0O0O ['password'],OOOO0O0OOO00O0O0O ['host'],OOOO0O0OOO00O0O0O ['db'])#line:895
        OOO0000O000OO0O0O =cx_Oracle .connect (O00OOO00OOO00O00O )#line:896
        try :#line:898
            OOOO00O0OOO000OOO =OOO0000O000OO0O0O .cursor ()#line:899
            print ("开始执行过程:{}  参数: {}".format (O00O0OO00O0O00OOO ,proc_para ))#line:900
            if proc_para is None :#line:901
                OO0OOOO00OO000000 =OOOO00O0OOO000OOO .callproc (O00O0OO00O0O00OOO )#line:902
                OOO0000O000OO0O0O .commit ()#line:903
            else :#line:904
                OO0OOOO00OO000000 =OOOO00O0OOO000OOO .callproc (O00O0OO00O0O00OOO ,proc_para )#line:906
                OOO0000O000OO0O0O .commit ()#line:907
            OOOO00O0OOO000OOO .close ()#line:908
            OOO0000O000OO0O0O .close ()#line:909
            print (OO0OOOO00OO000000 )#line:910
        except Exception as OO0O00O0O0O00OO0O :#line:911
            OOO0000O000OO0O0O .rollback ()#line:912
            OOO0000O000OO0O0O .close ()#line:913
            raise OO0O00O0O0O00OO0O #line:915
        return True #line:916
    def insert_contents_oracle (OO000O000OO0O0O0O ,O00OO00OO0O000O00 ,O00O00OOO00000O0O ,per_in =100 ,connect_dict =None ):#line:918
        import cx_Oracle #line:919
        OOO0OOOO0OO0OOO00 ='{}/{}@{}:{}/{}'.format (connect_dict ['user'],connect_dict ['password'],connect_dict ['host'],connect_dict ['port'],connect_dict ['db'])#line:925
        OOOO00OOOO0000OO0 =cx_Oracle .connect (OOO0OOOO0OO0OOO00 )#line:926
        O0OO00O0OO0OO0OOO =OOOO00OOOO0000OO0 .cursor ()#line:927
        O00O00OOOOO00000O =' into {} values {}'#line:928
        OOO000O00O0O00OO0 =''#line:929
        O0OO00000OOOO0000 =len (O00OO00OO0O000O00 )#line:930
        logging .info ("total {} records need to insert table {}: ".format (O0OO00000OOOO0000 ,O00O00OOO00000O0O ))#line:931
        try :#line:932
            for O0OOOOOO0O0OOO00O in range (O0OO00000OOOO0000 ):#line:933
                OOO000O00O0O00OO0 =OOO000O00O0O00OO0 +O00O00OOOOO00000O .format (O00O00OOO00000O0O ,tuple (O00OO00OO0O000O00 [O0OOOOOO0O0OOO00O ]))+'\n'#line:934
                if (O0OOOOOO0O0OOO00O +1 )%per_in ==0 or O0OOOOOO0O0OOO00O ==O0OO00000OOOO0000 -1 :#line:935
                    OOOO0O0000O000O0O ='insert all '+OOO000O00O0O00OO0 +'select 1 from dual'#line:936
                    logging .debug (OOOO0O0000O000O0O )#line:937
                    O0OO00O0OO0OO0OOO .execute (OOOO0O0000O000O0O )#line:938
                    OOOO00OOOO0000OO0 .commit ()#line:939
                    OOO000O00O0O00OO0 =''#line:940
            return str (O0OO00000OOOO0000 )#line:941
        except Exception as O000000O00O0O0OO0 :#line:942
            try :#line:943
                OOOO00OOOO0000OO0 .rollback ()#line:944
                O0OO00O0OO0OO0OOO .execute ("delete from {} where UPLOADTIME = '{}'".format (O00O00OOO00000O0O ,O00OO00OO0O000O00 [0 ][-1 ]))#line:945
                OOOO00OOOO0000OO0 .commit ()#line:946
            except Exception :#line:947
                logging .error ('can not delete by uploadtime')#line:948
            finally :#line:949
                raise O000000O00O0O0OO0 #line:950
        finally :#line:951
            OOOO00OOOO0000OO0 .close ()#line:952
class _O00OO000O0O0OO000 (object ):#line:956
    connect =None #line:957
    def __init__ (OOO000O0000O00OO0 ,O0OOO00O0O0OOO0OO ,O0OO000OO000OOOOO ,O00OO0OOOO0OOO0O0 ,offsets =None ):#line:959
        OOO000O0000O00OO0 .end_offset =None #line:960
        OOO000O0000O00OO0 .db_err_count =0 #line:961
        OOO000O0000O00OO0 .topic =O0OOO00O0O0OOO0OO #line:962
        OOO000O0000O00OO0 .kafkaconfig =O0OO000OO000OOOOO #line:963
        OOO000O0000O00OO0 .offsetDict ={}#line:964
        OOO000O0000O00OO0 .current_dir =O00OO0OOOO0OOO0O0 #line:965
        OOO000O0000O00OO0 .offsets =offsets #line:966
        try :#line:967
            OOO000O0000O00OO0 .consumer =OOO000O0000O00OO0 .connect_kafka_customer ()#line:968
        except Exception as O0O00OO0O0O0000O0 :#line:969
            O0O00OO0O0O0000O0 ='kafka无法连接','ErrLocation：{}\n'.format (O0OOO00O0O0OOO0OO )+str (O0O00OO0O0O0000O0 )+',kafka消费者无法创建'#line:970
            raise O0O00OO0O0O0000O0 #line:971
    def get_toggle_or_offset (O00O0OO00000O0OO0 ,OOOO0OOO00OO0OOO0 ,O0OOOOO000O0O0O00 ):#line:973
        ""#line:974
        if O00O0OO00000O0OO0 .offsets :#line:975
            if isinstance (O00O0OO00000O0OO0 .offsets ,int ):#line:976
                return O00O0OO00000O0OO0 .offsets #line:977
            else :#line:978
                O00OO00O0O00O000O =O00O0OO00000O0OO0 .offsets .get (str (O0OOOOO000O0O0O00 ))#line:979
                if O00OO00O0O00O000O is not None :#line:980
                    return int (O00OO00O0O00O000O )#line:981
        O00OO00O0O00O000O =0 #line:982
        try :#line:983
            O0OOO0O000OO0OOO0 =f"{O00O0OO00000O0OO0.current_dir}/kafka/{OOOO0OOO00OO0OOO0}_offset_{O0OOOOO000O0O0O00}.txt"#line:984
            if os .path .exists (O0OOO0O000OO0OOO0 ):#line:985
                OO0OOOO0OO0OOO00O =open (O0OOO0O000OO0OOO0 ).read ()#line:986
                if OO0OOOO0OO0OOO00O :#line:987
                    O00OO00O0O00O000O =int (OO0OOOO0OO0OOO00O )#line:988
            else :#line:989
                with open (O0OOO0O000OO0OOO0 ,encoding ='utf-8',mode ='a')as O0O0O0O00OOOOOO00 :#line:990
                    O0O0O0O00OOOOOO00 .close ()#line:991
        except Exception as OOO0OOOO0O0O00OOO :#line:992
            print (f"读取失败：{OOO0OOOO0O0O00OOO}")#line:993
            raise OOO0OOOO0O0O00OOO #line:994
        return O00OO00O0O00O000O #line:995
    def write_offset (O00O0OO000OOO000O ,O0OO0000O0OO00O00 ,offset =None ):#line:997
        ""#line:1000
        if O00O0OO000OOO000O .topic and offset :#line:1001
            O0O0O0OO00OOOO00O =f"{O00O0OO000OOO000O.current_dir}/kafka/{O00O0OO000OOO000O.topic}_offset_{O0OO0000O0OO00O00}.txt"#line:1003
            try :#line:1004
                with open (O0O0O0OO00OOOO00O ,'w')as OO00OO0O000OOO000 :#line:1005
                    OO00OO0O000OOO000 .write (str (offset ))#line:1006
                    OO00OO0O000OOO000 .close ()#line:1007
            except Exception as O0O00O00000O00O00 :#line:1008
                print (f"写入offset出错：{O0O00O00000O00O00}")#line:1009
                raise O0O00O00000O00O00 #line:1010
    def connect_kafka_customer (OOO0O000000OO0OOO ):#line:1012
        ""#line:1013
        OOO0OOO0OOOOO000O =KafkaConsumer (**OOO0O000000OO0OOO .kafkaconfig )#line:1014
        return OOO0OOO0OOOOO000O #line:1015
    def parse_data (O000OO0O000O00OOO ,O000O00000OO0O0O0 ):#line:1017
        ""#line:1022
        return dict ()#line:1023
    def gen_sql (OO0OO00OO0000OOOO ,OOO0OO0OOOOOO00OO ):#line:1025
        ""#line:1030
        OOO00OOOOO000O0OO =[]#line:1031
        for O0OO00O0O0O0O00O0 in OOO0OO0OOOOOO00OO :#line:1032
            OOO00OOOOO000O0OO .append (str (tuple (O0OO00O0O0O0O00O0 )))#line:1034
        return ','.join (OOO00OOOOO000O0OO )#line:1035
    def dispose_kafka_data (O0OO0O0000000O00O ,O0O00OOOO0000OOOO ):#line:1037
        ""#line:1042
        pass #line:1043
    def get_now_time (OOOOO0O00O0OOO000 ):#line:1045
        ""#line:1049
        O00OOOO000OOOOO00 =int (time .time ())#line:1050
        return time .strftime ('%Y-%m-%d %H:%M:%S',time .localtime (O00OOOO000OOOOO00 ))#line:1051
    def tran_data (O00O0OO00OOO0OOO0 ,O0O0000O0000000O0 ,OOO000000000000O0 ):#line:1053
        ""#line:1059
        OOO000OOO000OO0O0 =O0O0000O0000000O0 .get (OOO000000000000O0 ,"")#line:1060
        OOO000OOO000OO0O0 =""if OOO000OOO000OO0O0 is None else OOO000OOO000OO0O0 #line:1061
        return str (OOO000OOO000OO0O0 )#line:1062
    def consumer_data (OO000OO00000OO00O ,O0O000O0OO00OOO00 ,OOOO0OO0OOO0OOO0O ,O000O000OO0OO00O0 ):#line:1064
        ""#line:1071
        if OO000OO00000OO00O .consumer :#line:1072
            OO000OO00000OO00O .consumer .assign ([TopicPartition (topic =OO000OO00000OO00O .topic ,partition =O0O000O0OO00OOO00 )])#line:1073
            O000OO00OOO00000O =TopicPartition (topic =OO000OO00000OO00O .topic ,partition =O0O000O0OO00OOO00 )#line:1075
            O000O000OO00O0000 =OO000OO00000OO00O .consumer .beginning_offsets ([O000OO00OOO00000O ])#line:1076
            O0O0OO00O000OOO0O =O000O000OO00O0000 .get (O000OO00OOO00000O )#line:1077
            O0OOO0O0O0OO00O00 =OO000OO00000OO00O .consumer .end_offsets ([O000OO00OOO00000O ])#line:1078
            O00OO00000OO0O0O0 =O0OOO0O0O0OO00O00 .get (O000OO00OOO00000O )#line:1079
            print (f'建立消费者, {O0O000O0OO00OOO00}分区, 最小offset:{O0O0OO00O000OOO0O}, 最大offset:{O00OO00000OO0O0O0}')#line:1080
            if OOOO0OO0OOO0OOO0O =='-996':#line:1081
                OOOO0OO0OOO0OOO0O =O0OOO0O0O0OO00O00 -1 #line:1082
            if OOOO0OO0OOO0OOO0O <O0O0OO00O000OOO0O :#line:1083
                print (f'Warning: 消费offset：{OOOO0OO0OOO0OOO0O} 小于最小offset:{O0O0OO00O000OOO0O}')#line:1084
                OOOO0OO0OOO0OOO0O =O0O0OO00O000OOO0O #line:1085
            if OOOO0OO0OOO0OOO0O >=O00OO00000OO0O0O0 :#line:1086
                print (f'消费offset：{OOOO0OO0OOO0OOO0O} 大于最大offset:{O00OO00000OO0O0O0}, 本次不消费')#line:1087
                return #line:1088
            OO000OO00000OO00O .end_offset =O00OO00000OO0O0O0 #line:1089
            OO000OO00000OO00O .consumer .seek (TopicPartition (topic =OO000OO00000OO00O .topic ,partition =O0O000O0OO00OOO00 ),offset =OOOO0OO0OOO0OOO0O )#line:1090
            print (f'消费{O0O000O0OO00OOO00}分区, 开始消费offset：{OOOO0OO0OOO0OOO0O}!')#line:1091
            O000O0O00O000OO00 =O000O000OO0OO00O0 (OO000OO00000OO00O .consumer )#line:1092
            OOOO0OO0OOO0OOO0O =O000O0O00O000OO00 .offset +1 #line:1093
            OO000OO00000OO00O .offsetDict [O0O000O0OO00OOO00 ]=OOOO0OO0OOO0OOO0O #line:1096
            OO000OO00000OO00O .write_offset (O0O000O0OO00OOO00 ,OOOO0OO0OOO0OOO0O )#line:1097
            OO000OO00000OO00O .offsetDict [O0O000O0OO00OOO00 ]=OOOO0OO0OOO0OOO0O #line:1100
            OO000OO00000OO00O .write_offset (O0O000O0OO00OOO00 ,OOOO0OO0OOO0OOO0O )#line:1101
    def consumer_topic (O0000OO0OOOOO000O ,OOO0O00OO0O00O00O ):#line:1103
        print (f"topic: {O0000OO0OOOOO000O.topic}")#line:1104
        print ('开始解析。')#line:1105
        O00OO00OO0OOO0000 =O0000OO0OOOOO000O .consumer .partitions_for_topic (topic =O0000OO0OOOOO000O .topic )#line:1107
        for O0O0OOO0OOOO00O00 in O00OO00OO0OOO0000 :#line:1108
            OO00OO0OOO0O00000 =O0000OO0OOOOO000O .get_toggle_or_offset (O0000OO0OOOOO000O .topic ,O0O0OOO0OOOO00O00 )#line:1109
            O0O0000OO0O000OO0 =0 if OO00OO0OOO0O00000 <0 else OO00OO0OOO0O00000 #line:1111
            O0000OO0OOOOO000O .consumer_data (O0O0OOO0OOOO00O00 ,O0O0000OO0O000OO0 ,OOO0O00OO0O00O00O )#line:1112
    def save_all_offset (OO0OO0000OO00O00O ):#line:1114
        for O0OOO0OO000OO0000 ,O0OO0000OO0000OO0 in OO0OO0000OO00O00O .offsetDict :#line:1115
            OO0OO0000OO00O00O .write_offset (O0OOO0OO000OO0000 ,O0OO0000OO0000OO0 )#line:1116

import os 
import sys
import re
import genClasses
import random
try:
    import requests
    import json
except:
    pass
import traceback
from .SystemConfig import USER_CONFIG
import SQLModel
import LogParser
class InfoModel:
    def __init__(self):
        '''
        'SOURCE'    : SOURCE,          #Design, Customer
        'JOB_ID'    : 12345678, 
        'JOB_NAME'  : JOB_NAME,
        'USER_NAME' : pc_name-cam_name,
        'EXEC_ID'   : '3345678',
        'PROGRAM'   : PROGRAM_NAME,
        'PROGRAM_VER' : 'TEST',        #yymmdd
        'SOFTWARE'    : SOFTWARE,      #incam, genesis, ezcam
        'EXEC_MODE'   : 'Manual',      #Manual, Auto
        'TR_VER'      : 'Test',        #Test, Release
        'DATABASE'    : 'Dev',         #User, Dev ; all execution without MainUi would be recorded in 'Dev'
        'LOG_PATH'    : LOG_PATH       #
        '''
        pass
        self.root_path = os.environ['ROOT_PATH'] 

    def get_attr(self, TR_ver = None, gen_object = None):
        self.gen_object = gen_object
        self.get_gen_object()
        
        self.get_user_name()
        self.get_privilage()
        self.get_TR_ver(TR_ver)
        self.get_DB() 
        self.get_software()
        self.get_job_name()
        self.get_job_id()
        self.get_source()
    # ================== base info ==================== #
    def get_gen_object(self):
        try:
            if self.gen_object is not None:
                return self.gen_object
            # os.environ['JOB'] = 'real-lb021j-juri-bd'
            elif 'JOB' in os.environ.keys():
                self.gen_object = genClasses.Job(os.environ['JOB'])     
            else:
                self.gen_object = genClasses.Top()
        except Exception as e:
            self.gen_object = None
            print(e)
        return self.gen_object

    def get_user_name(self):
        cam_user = 'gateway'
        if self.gen_object is not None:
            self.gen_object.COM('get_user_name')
            cam_user = self.gen_object.COMANS

        
        pc_user = '9527' if 'USER' not in os.environ.keys() else os.environ['USER'] 


        self.user_name = '{0}-{1}'.format(pc_user,cam_user) 
        return self.user_name



    def get_privilage(self):
        # IES_USERLIST = ['210605', '210814', '220741', '220853', '220741', 'IESAdmin'] 
        pc_user = self.user_name.split('-')[0]
        if pc_user in USER_CONFIG['DEV_PC_ID'] or self.user_name == 'incam-incam' or self.user_name == 'genesis-patrick':
            self.privilage = 'Dev'
        elif 'keddy' in self.user_name.lower():
            self.privilage = 'Supervisor'
        else:
            self.privilage = 'User'
        return self.privilage
    

    def get_TR_ver(self, _TR_ver = None):
        if _TR_ver:
            self.TR_ver = _TR_ver
        else:
            self.TR_ver = 'Test'
        return self.TR_ver

    def get_DB(self):
        if self.privilage == 'Dev':
            self.DB = 'Dev'
        elif self.TR_ver == 'Test':
            self.DB = 'Test'
        else: #only TR_ver == 'Release' and privilage != 'Dev'
            self.DB = 'User' 
        return self.DB
    # ================== default info ==================== #

    # ==================== cam info ====================== #


    def get_software(self):
        if 'Debugger' not in os.environ['GEN_PATH']:
            # get version
            self.gen_object.COM('get_version')
            ver = self.gen_object.COMANS
            if 'incam' in ver.lower():
                software = 'incam'
            else:
                if 'win' in sys.platform.lower():
                    software = 'ezcam'    
                else:
                    software = 'genesis'
        else:
            if 'win' in sys.platform.lower():
                software = 'ezcam'   
            else:
                software = 'incam'
        self.software = software
        return software


    def get_job_name(self):
        if 'JOB' in os.environ.keys() and os.environ['JOB']:
            self.job_name = os.environ['JOB']
        else:
            self.job_name = 'Unknown' 
        return self.job_name


    def get_source(self):
        self.source = 'hi_i_am_source' 
        is_gerber = False
        JOB_NAME = self.job_name.upper()
        # JOB_NAME = 'real-lb021j-a1d01'
        # JOB_NAME = 'rd-202300256-a1d01'
        if JOB_NAME == 'Unknown'.upper():
            self.source = 'Na'
            return self.source
        my_data = {'job_name' : JOB_NAME}
        try:
            if sys.version_info[0] + 0.1 * sys.version_info[1] < 2.6:
                text = 'curl -d "job_name=%s" -X POST %scam/call_check_is_gerber' %\
                    (my_data["job_name"], os.environ['NORMAL_SERVICE'])
                echo_stdout = os.popen(text, 'r').read()
                is_gerber = eval(echo_stdout)
            else:
                url = os.environ['NORMAL_SERVICE'] + 'cam/call_check_is_gerber'
                r = requests.post(url,
                                data=my_data, timeout=10)
                is_gerber = eval(r.text)
            if is_gerber:
                self.source = 'Customer'
                return self.source
            else:
                self.source = 'Design'
                return self.source
        except:
            self.source = 'Na'
            return self.source
    
    def get_job_id(self):
        '''get one or create one if not exist'''

        job_id = '404'
        if 'JOB' in os.environ.keys() and os.environ['JOB']:
            
            # gen_object = genClasses.Job(os.environ['JOB'])    
            attr_dict = self.gen_object.DO_INFO('-t job -e {0} -d ATTR'.format(self.gen_object.name))
            
            if '.comment' in attr_dict['gATTRname']:
                idx = attr_dict['gATTRname'].index('.comment')
                comment = attr_dict['gATTRval'][idx]
            else:
                comment = ''
            if '404' in comment or not comment:
                job_id = str(random.randint(1000000, 9999999))
                comment_text = "job_id={0};".format(job_id)
                self.gen_object.COM("set_attribute, attribute=.comment, \
                                job={0},name1=,type=Job,value={1}".format(self.gen_object.name, comment_text))
            else:
                comment_list = comment.split(';')
                for var in comment_list:
                    if 'job_id' in var:
                        job_id = var.split('=')[1]
                        break 


            self.job_id = job_id
        else:                
            job_id = str(404)
            self.job_id = job_id
        return self.job_id
        
    def pack_exec_info(self, exec_mode):
        exec_info = {
            "JOB_ID" : self.job_id,
            "JOB_NAME" : self.job_name,
            "USER_NAME" : self.user_name,
            "EXEC_ID" : str(random.randint(100000,999999)),
            "LOG_PATH" : '',
            "PROGRAM" : '',
            "PROGRAM_VER" : '',
            "SOFTWARE" : self.software,
            "EXEC_MODE" : exec_mode,
            "TR_VER" : self.TR_ver,
            "DATABASE" : self.DB,
            "SOURCE" : self.source,
        }

        return exec_info
    '''
     class ob :
        def __init__(self):
            pass

     self = ob()

    '''
    def load_program_config(self):
        try:
            if os.path.isfile("program_config.json"):
                with open("program_config.json", "r") as file:
                    config = json.load(file)
                    # print(config)
                return config    
            else:
                with open("program_config.json", "w") as file:
                    json.dump({}, file, indent=4)
                print('no program_config.json')
                return {}
        except Exception as e:
            err_msg = traceback.format_exc()
            print(err_msg)
            print('Failed to load program_config' )
            return {} 


    def load_param_config(self):
        '''
        
        '''
        job_id = self.job_id
        job_name = self.job_name
        folder_path = os.path.join('JobDatabase', job_id + '-' + job_name)
        file_path = os.path.join(folder_path, 'JOB_parameter_config.json')
        if os.path.isfile(file_path): 
            with open("JOB_parameter_config.json", "r") as file:
                self.param_config = json.load(file)

        else:
            self.param_config = {}
        return self.param_config
    
    def load_init_program_log(self):

        # load from db
        job_init_program_log = {}

        # db_job_logs_dict = load_job_logs_from_db('Dev', 'Test','2640439')
        db_job_logs_dict = SQLModel.load_job_logs_from_db(self.DB, self.TR_ver, self.job_id, self.job_name)
        if 'ProgramName' in db_job_logs_dict.keys():    #ensure data more than one.
            for key, program_name in db_job_logs_dict['ProgramName'].items():
                job_init_program_log[program_name] = {}
                job_init_program_log[program_name]['ProgramState'] = db_job_logs_dict['ProgramState'][key]
                job_init_program_log[program_name]['ExecID'] = db_job_logs_dict['ExecID'][key]

        # load from tmp_job_log
        tmp_job_logs = LogParser.load_tmp_db_logs(self.root_path,
                                                   self.job_id,
                                                   self.job_name)


        for tmp_job_log_dict in tmp_job_logs:
            # tmp_job_log_dict = eval(tmp_job_log)

            program_name  = tmp_job_log_dict['ProgramName']
            if program_name not in job_init_program_log.keys():
                job_init_program_log[program_name] = {}    
            job_init_program_log[program_name]['ProgramState'] = tmp_job_log_dict['ProgramState']
            job_init_program_log[program_name]['ExecID'] = tmp_job_log_dict['ExecID']
        return job_init_program_log

    def load_history_db_logs(self):
        history_db_logs_dict = {}
        
        perm_db_txt_logs = SQLModel.load_perm_db_txt_log(self.DB, self.TR_ver, self.job_id, self.job_name)
        for tmp_db_log in perm_db_txt_logs:
            if tmp_db_log['ProgramName'] not in history_db_logs_dict.keys():
                history_db_logs_dict[tmp_db_log['ProgramName']] = []
            if 'LogMsg' not in tmp_db_log.keys() :
                continue
            history_db_logs_dict[tmp_db_log['ProgramName']].append( tmp_db_log )




        tmp_db_logs = LogParser.load_tmp_db_logs(
            self.root_path, self.job_id, self.job_name )
        for tmp_db_log in tmp_db_logs:
            if tmp_db_log['ProgramName'] not in history_db_logs_dict.keys():
                history_db_logs_dict[tmp_db_log['ProgramName']] = []
            if 'LogMsg' not in tmp_db_log.keys() :
                continue
            history_db_logs_dict[tmp_db_log['ProgramName']].append( tmp_db_log )

                # frame = self.findChild(ProgramFrame, tmp_db_log['ProgramName'])
                # frame.update_execute_log(tmp_db_log)
        return history_db_logs_dict
    def load_readme(self, ver_folder_path):
        readme_info = {'project_name':'',
                       'description':'',
                       'release_log':''}
        readme_path = os.path.join(ver_folder_path, 'readme.md')

        if not os.path.isfile(readme_path):
            return {}

        with open(readme_path, 'r') as f:
            readme = f.read()


        text = readme
        # Find all section headings and their contents
        sections = re.findall(r'# (.*?)\n(.*?)(?=# |\Z)', text, re.DOTALL)

        # Define the sections you want to include
        wanted_sections = ['Project', 'Project Goal', 'Release Log']
        title_map = {'Project': 'project_name',
                    'Project Goal' : 'description',
                    'Release Log': 'release_log'}

        # Create a dictionary for the wanted sections using a for loop
        
        for title, content in sections:
            if title in wanted_sections:
                readme_info[title_map[title]] = content.strip()

        # Parse Release Log
        raw_log_list = readme_info['release_log'].split('\n')
        
        
        date_desc_list = []
        for log in raw_log_list:
            if log:
                date = log.split(' ')[1]
                description = ' '.join(log.split(' ')[2:])
                date_desc_list.append([date, description])
        
        readme_info['release_log'] = ''
        for log in date_desc_list:
            log = ' : '.join(log)
            readme_info['release_log'] += log + '\n'
        return readme_info
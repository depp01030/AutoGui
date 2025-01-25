import os 
import sys 
import traceback 
import genClasses 

from mainWindow.InfoModel import InfoModel

#%% 
def init_job_object(job_name):
    os.environ['JOB'] = job_name
    print('*************************************')
    print(job_name)
    print('*************************************')
    job_object = genClasses.Job(job_name)
    #open job
    job_object.COM('open_job,job={0}'.format(job_name))
    job_object.COM('clipb_open_job,job={0},update_clipboard=view_job'.format(job_name))
    return job_object


def save_n_close(job_object):

    # close job 
    # job_object.COM('save_job,job={0},override=no,skip_upgrade=no,\
    #                 upgradeToInCAMPro=yes'.format(job_object.name)) 
    job_object.COM('check_inout,job={0},mode=in,type=job'.format(job_object.name)) 
    job_object.COM('close_job,job={0}'.format(job_object.name)) 


def layer_exists_checker(step_object, layer_name):
   isLayer = False
   matrix_dict =  step_object.job.matrix.getInfo()
   all_layer_name_list = matrix_dict["gROWname"]
   if layer_name in all_layer_name_list:
       isLayer = True
   return isLayer
def reset_tmp_layer(step_object, tmp_layer_name):
   isLayer = layer_exists_checker(step_object, tmp_layer_name)
   if isLayer == False:
       step_object.COM("create_layer,layer=%s,context=misc,type=signal,polarity=positive,\
                       ins_layer=" % (tmp_layer_name))
   else:
       step_object.COM("delete_layer,layer={0}".format(tmp_layer_name))
       step_object.COM("create_layer,layer=%s,context=misc,type=signal,polarity=positive,\
                       ins_layer=" % (tmp_layer_name))

def do_batch_tasks(job_name, parent, program_wait_queue):
    try:
        job_object = init_job_object(job_name)



        matrix_dict = job_object.matrix.getInfo()
        step_list = matrix_dict['gCOLstep_name']
        step_name = step_list[0]

        step_object = genClasses.Step(job_object, step_name)  
        reset_tmp_layer(step_object, 'test_layer') 
        info_model = InfoModel()
        info_model.get_attr(TR_ver = parent.TR_ver,
                            gen_object = job_object)
        exec_info = info_model.pack_exec_info(exec_mode = 'Auto')
        parent.exec_program_queue(exec_info = exec_info, 
                                  program_wait_queue = program_wait_queue)
        # state_code = '200'
        # ''' ===================== run program ===================== '''


        # for frame in program_wait_queue:   
            
        #     exec_info["LOG_PATH"] = os.path.join(parent.root_path, frame.main_folder_path, 'Tmp')  
        #     exec_info["PROGRAM"] = frame.program_name
        #     file_path = frame.get_exec_file_path()
        #     exec_info["PROGRAM_VER"] = frame.current_ver
            
        #     if state_code[0] != '5' or exec_info["EXEC_MODE"] == 'Test': #not 5xx  
        #         state_code = frame.run(exec_info) 
        #         # msg = '[Info] : Program {0} Finish \n'.format(frame.program_name)
        #         # self.LogBox.append(msg)
    



    except Exception as e:
        
        err_msg = traceback.format_exc() 
        print(err_msg)





    save_n_close(job_object)
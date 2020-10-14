import yaml
import sys

P_VALUE = 10.0
I_VALUE = 10.0
D_VALUE = 0.0

def generate_numberelementsfile(num_elements, num_elements_filename):

    data = [str(num_elements)]
    fill_file_with_data(data, num_elements_filename)


def generate_controllerargs_dict(num_elements):
    """
    Generate All the controle arguments based on the number of elements
    """
    
    data = []

    for x in range(0, num_elements):
        aux_controller_name = "snake_body_"+str(x)+"_aux_joint_position_controller"
        main_controller_name = "snake_body_"+str(x)+"_joint_position_controller"
        data.append(aux_controller_name)
        data.append(main_controller_name)
    
    data.append("joint_state_controller")
    data.append("--shutdown-timeout 3")
    
    return data


def generate_controllerconfig_yaml_dict(num_elements):
    """
    Generate the dict for the yaml config file for the controle
    
    """
    name_space = 'snake'
    publish_rate = 50
    

    """
    data = {name_space:
                {   'joint_state_controller':{'type':'joint_state_controller/JointStateController',
                                            'publish_rate':publish_rate
                                            },
                    'snake_body_0_aux_joint_position_controller':{  'type':'effort_controllers/JointPositionController',
                                                                    'joint':'snake_body_0.0_aux_joint',
                                                                    'pid':dict(p = 3.0, i = 1.0, d = 0.0)
                                                                },
                    'snake_body_0_joint_position_controller':{  'type':'effort_controllers/JointPositionController',
                                                                'joint':'snake_body_0.0_aux_joint',
                                                                'pid':dict(p = 3.0, i = 1.0, d = 0.0)
                                                                },
                    
                }
            }
            
    """
    
    content_dict = {   'joint_state_controller':{'type':'joint_state_controller/JointStateController',
                                            'publish_rate':publish_rate
                                            },
                    }
                    
    
    for x in range(0, num_elements):
        # TODO: Fixed due to change in kinetic
        #float_string_value = str(float(x))
        float_string_value = str(int(x))
        int_string_value = str(x)
        
        aux_controller_name = 'snake_body_'+int_string_value+'_aux_joint_position_controller'
        
        aux_controller_data_dict = {'type':'effort_controllers/JointPositionController',
                                'joint':"snake_body_"+float_string_value+"_aux_joint",
                                'pid':dict(p = P_VALUE, i = I_VALUE, d = D_VALUE)
                                }
                                
        controller_name = 'snake_body_'+int_string_value+'_joint_position_controller'
        
        controller_data_dict = {'type':'effort_controllers/JointPositionController',
                                'joint':"snake_body_"+float_string_value+"_joint",
                                'pid':dict(p = P_VALUE, i = I_VALUE, d = D_VALUE)
                                }
        
        content_dict[aux_controller_name] = aux_controller_data_dict
        content_dict[controller_name] = controller_data_dict
    
    
    data = {name_space:content_dict}
            

    return data
    

def generate_controllerargsfile(num_elements, controllerargs_filename):


    data = generate_controllerargs_dict(num_elements)
    fill_file_with_data(data, controllerargs_filename)
    
def generate_controllerconfig_yamlfile(num_elements, controllerconfig_yaml_filename):

    data = generate_controllerconfig_yaml_dict(num_elements)
    fill_yaml_with_datadict(data, controllerconfig_yaml_filename)
    

def fill_file_with_data(data, filename):
    
    with open(filename, 'w') as outfile:
        for element in data:
            data_to_write = element + "\n"
            outfile.write(data_to_write)    
            
def fill_yaml_with_datadict(data, yamlfilename):
    
    with open(yamlfilename, 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False) 

if __name__ == "__main__":
    
    
    
    num_elements = int(sys.argv[1])
    print(str(num_elements))
    
    generate_numberelementsfile(num_elements=num_elements, num_elements_filename='numelements_temp.yaml')
    generate_controllerargsfile(num_elements=num_elements, controllerargs_filename='controllerargs_temp.yaml')
    generate_controllerconfig_yamlfile(num_elements=num_elements, controllerconfig_yaml_filename='snake_full_control_temp.yaml')
    

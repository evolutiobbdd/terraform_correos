import sys
import os
import shutil
import json
from python_terraform import *

script_dir="/mnt/c/Users/200000325/Documents/terraform/upgrade_script"
working_dir = sys.argv[1]
var_cluster_id = sys.argv[2]
var_upgrade_version = sys.argv[3]
terraform_working_dir=script_dir+"/tmp/"+working_dir
print("Terraform working directory: "+terraform_working_dir)
os.makedirs(terraform_working_dir)

#copy tf files to terraform working directory
shutil.copy(script_dir+'/provider.tf', terraform_working_dir)
shutil.copy(script_dir+'/terraform.tfvars', terraform_working_dir)
shutil.copy(script_dir+'/vars.tf', terraform_working_dir)

#replace cluster id in new main.tf import template
input_file = open(script_dir+"/import_template.tf", "rt")
output_file = open(terraform_working_dir+"/main.tf", "wt")
for line in input_file:
    output_file.write(line.replace('cluster_identifier_name', var_cluster_id))
input_file.close()
output_file.close()

#import current cluster to terraform
tf = Terraform(working_dir=terraform_working_dir)
tf.cmd('init', capture_output=False)
tf.cmd('import', 'aws_rds_cluster.'+var_cluster_id, var_cluster_id, capture_output=False)
tf.cmd('state show', 'aws_rds_cluster.'+var_cluster_id, capture_output=False)

#get engine value from cluster state
return_code, stdout_cluster_settings, stderr = tf.cmd('show', '-json', 'terraform.tfstate')
var_cluster_settings = json.loads(stdout_cluster_settings)
var_engine=var_cluster_settings['values']['root_module']['resources'][0]['values']['engine']

#delete current main.tf
os.remove(terraform_working_dir+"/main.tf")

#create new main.tf with changes to run terraform plan 
#replace values in main.tf import template
#replace values in main.tf import template
input_file = open(script_dir+"/new_plan_template.tf", "rt")
output_file = open(terraform_working_dir+"/main.tf", "wt")
checkWords = ("cluster_identifier_name","curr_engine","new_version")
repWords = (var_cluster_id, var_engine, var_upgrade_version)

for line in input_file:
    for check, rep in zip(checkWords, repWords):
        line = line.replace(check, rep)
    output_file.write(line)
input_file.close()
output_file.close()

#terraform plan 
tf.cmd('plan', capture_output=False)
print("")
print("######################################################")
print("IF terraform plan IS OK:")
print("cd "+terraform_working_dir)
print("terraform apply")


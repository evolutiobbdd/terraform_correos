# terraform_correos
 
upgrade_cluster.py es un script en python para realizar un minor upgrade de un cluster Aurora PostgreSQL en AWS usando Terraform (utiliza el módulo python-terraform como wrapper). 

Modo de Uso:

upgrade_cluster.py <terraform_working_directory> <cluster_db_identifier> <nueva_versión>

Por ej., 

upgrade_cluster.py test1 awir-l-maestros-rds-dbcluster-01-cluster 11.15

Esta ejecución creará un directorio en upgrade/tmp/test1 en donde se realizará el terraform init, terraform import, etc.

Estructura del repositorio: 

```bash
 upgrade
├── import_template.tf
├── new_plan_template.tf
├── provider.tf
├── terraform.tfvars
├── tmp
├── upgrade_cluster.py
└── vars.tf
```

Pasos realizados por el script: 

- se supone que el cluster no está en terraform, por lo que se crea un nuevo directorio y se hace el import en donde se crea el archivo terraform.tfstate con la configuración. Para esto se usa el import_template.tf que se copia al directorio temporal de terraform como main.tf con el cluster db identifier que se pasó como parámetro
- una vez hecho el import, se reemplaza el main.tf usando el new_plan_template.tf para hacer un nuevo main.tf con la nueva versión del cluster
- se ejecuta el terraform plan
- si el terraform plan es considerado ok, se imprimen en pantalla los comandos para ejecutar el terraform apply. Este script NO ejecuta el terraform apply. 


Conexión a AWS:

- en provider.tf se define la región, el profile y la ubicación del archivo de credentials (variable credential_file)
- en vars.tf se define la variable credential_file de tipo list
- en vars.tf se inicializa la variable credential_file


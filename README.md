# Xgrid Task
![alt text](https://www.pasha.org.pk/pashapk/2019/07/xgrid-logo-1.png?raw=true)


***

- Setup AWS profile .
- Create AWS CLoudformation stack.
- Server and access the service.


## Overview

- *Clone the repository*
- *Generate an AWS key pair if you don't have one*
- *Download account access keys csv from the aws IAM dashboard*- 
- *Create AWS Cloudformation stack for infrastructure proisioning through appStack.yml*
- *Tranfser source to EC2 instance and replace database hostname in index.py.*
- *Cofigure apache2 to run cgi scripts from root directory*
- *Connect with rds instance from EC2 and populate database using dummy_db.sql*
- *Restart apache2 service*
- *Access the service by navigating to http://<EC2-ElasticIP>*
- *Generate PDF*


---


## Clone Project

```sh
https://github.com/Noman-Ali-Bajwa/xgrid-task.git
cd xgrid-task/
```
---

## aws-cli Access
```sh
aws configure --profile test
#Enter the access key:
#Enter the secret access key:
#Enter default region:
#Enter output format:
```
---
So you've configured an aws porfile now which will later be used.
## Create Cloudformation Stack.
>Navigate to the Stack_templates directory , open AppStack.yml in an editor
>Replace the value of "key" with the name of the your account key-pair (.pem file)
```sh
aws cloudformation create-stack --stack-name appStack --template-body file://\$PWD/AppStack.yml --profile test --region us-east-1

```
>Wait for some moments , you'll be returned a stack_id indicating the initialization of cloudformation stack creation.
![alt text](https://github.com/Noman-Ali-Bajwa/xgrid-task/blob/main/stack_created.png?raw=true)
>Navigate to aws web management console cloudformation dashboard to view the stack status.
>You may navigate to resources tab and confirm the creation of all the resources (may take some time).
![alt text](https://github.com/Noman-Ali-Bajwa/xgrid-task/blob/main/appStack_dashboard.png?raw=true)
       
       

>After all the resources have been created, navigate to the outputs tab and note down the EC2 instance ElasticIP and >Database connection string.
![alt text](https://github.com/Noman-Ali-Bajwa/xgrid-task/blob/main/appStack_outputs.png?raw=true)
---
## Copy project files to the EC2 instance.
```sh
scp -r -i <path-to-pem_file> ./xgrid-task/source/  ubuntu@<EC2_IP>:/home/ubuntu/
```

```sh
ssh -i <path-to-pem_file> ubuntu@<EC2_IP>
sudo su
cd source/
mv index.py /var/www/html/
chown -R www-data:www-data index.py
chmod +x index.py
# Populate database appDB.
mysql -h <JDBC-connection_string-from-Cloudfornation-outputs> -u adminadmin -appDB -p < dummy_DB.sql
#Enter Password: password123
```
---

## Serve python script as cgi script on apache2.

```sh
nano /etc/apache2/apache2.conf
```
>Now we can check the status of our replica set created by the deployment and the pods there in a number of ways.
>Find the </Directory> tag in the file and overwrite the whole block with the following block.
```
<Directory />
       Options FollowSymLinks Indexes ExecCGI
        AddHandler cgi-script .py
        AllowOverride None
        Require all denied
</Directory>
<Directory /usr/share>
        AllowOverride None
        Require all granted
</Directory>
<Directory /var/www/>
        Options Indexes FollowSymLinks ExecCGI
        AddHandler cgi-script .py
        AllowOverride None
        Require all granted
</Directory>
```

---
## Disable directory listing on Apache2.
>You may want to access the service directly from the IP and not through a directory listing and directory listings being a security threat as well we will change the DocumentRoot directive.
```sh
nano /etc/apache2/sites-available/000-default.conf
# change the DocumentRoot directive to as shown below.
```
```
> DocumentRoot /var/www/html/index.py
```
---
```sh
#restart apache2 service.
systemctl restart apache2
```
---

>Now you may access the service by navigating to http://<EC2instance_ElasticIP>
Apply the date filter.
Click the download as PDF button.
*Since dummy data has been used , for the sake of demo it is suggested to give a date range between [12-10-2021 - 12-31-2021]*
---


Django study enrollment
=======================

[This project is in development. The README.md is written to guide development of its features and should be considered aspirational.]

This project is intended to be a stand-alone website that research studies
can use to implement online enrollment process for study participants. Our model
for this comes from the enrollment process used by the Personal Genome Project,
which places strong emphasis on having a highly informed cohort.

To clarify roles in our instructions below: "users" refers to potential study
participants, and "researchers" refers to researchers and other people with
administrative access to user information.

Enrollment processes supported by this software
-----------------------------------------------

This software assumes the following enrollment process:

1. (optional) Eligibility questions: A series of questions is presented to the potential enrollee. If eligibility requirements are met, the user is invited to step 2.
2. The user creates an account by entering their email address.
3. This email address is validated and an account is created.
4. (optional) The user logs in and is presented with an enrollment exam. This may contain multiple modules; once a module is passed it is recorded (i.e. progress is not lost if the user logs out).
5. The user is presented with the consent form and electronically signs it by typing his/her name.
6. (optional) Simple information collection. (e.g. addresses)
7. The user is done and gets emailed a copy of the consent form. The study takes it from here.

Installation
------------

This software is intended to be easily used in cloud infrastructure, eliminating the need for acquiring access to a server locally.

Our instructions will cover hosting an instance of this software on Amazon Web Services.

###Sign Up for AWS

When you sign up for Amazon Web Services (AWS), your AWS account is automatically signed up for all services in AWS.  

To create an AWS account  
Go to [http://aws.amazon.com](http://aws.amazon.com), and then click Sign Up.  
Follow the on-screen instructions.  
Part of the sign-up procedure involves receiving a phone call and entering a PIN using the phone keypad.  

###Setup AWS command line tools

One of the quickest ways to get started is to use Amazon's Elastic Beanstalk.  Elastic Beanstalk allows quick creation and management of multiple AWS services.

To get started download the command line interface (cli) tools for Elastic Beanstalk (eb).

[http://aws.amazon.com/code/6752709412171743](http://aws.amazon.com/code/6752709412171743)

Simply unzip the download zip file ("/home/yourusername/bin/" is a good spot) and add to your path the location of the eb executable. (e.g. add the following line to your .bashrc)

    export PATH=$PATH:/home/yourusername/bin/AWS-ElasticBeanstalk-CLI-2.6.0/eb/linux/python2.7/

Then:

    source ~/.bashrc

###Get django_study_enrollment project

Clone this repository 

    git clone https://github.com/OpenHumans/django_study_enrollment.git
    cd django_study_enrollment



Now initate Elastic Beanstalk for this repo
 
    [yourusername@yourmachine django_study_enrollment]$ eb init



You'll be prompted for several pieces of information.  
You'll first be asked for your AWS Access Key ID and Secret Access Key.

    To get your AWS Access Key ID and Secret Access Key, 
      visit "https://aws-portal.amazon.com/gp/aws/securityCredentials".
    Enter your AWS Access Key ID: AKIAIExampleKey
    Enter your AWS Secret Access Key: yYGyhXTt27ulESpoInXTlymb60mExampleKey



Then you'll be prompted for a service region, here we've selected US East.

    Select an AWS Elastic Beanstalk service region.
    Available service regions are:
    1) US East (Virginia)
    2) US West (Oregon)
    3) US West (North California)
    4) EU West (Ireland)
    5) Asia Pacific (Singapore)
    6) Asia Pacific (Tokyo)
    7) Asia Pacific (Sydney)
    8) South America (Sao Paulo)
    Select (1 to 8): 1



Now you'll be asked for an appliation name and environment name, here we've selected the auto generated value.

    Enter an AWS Elastic Beanstalk application name (auto-generated value is "django_study_enrollment"): 
    Enter an AWS Elastic Beanstalk environment name (auto-generated value is "djangostudyenrollment-e"): 



An environment tier selection is required next.  We need just a standard WebServer.

    Select an environment tier.
    Available environment tiers are:
    1) WebServer::Standard::1.0
    2) Worker::SQS/HTTP::1.0
    Select (1 to 2): 1



Next a solution stack selection is required.
There are many prebuilt stacks availble, but we will use **"32bit Amazon Linux 2013.09 running Python 2.7"** for this project (option 19).

    Select a solution stack.
    Available solution stacks are:
    1) 32bit Amazon Linux 2013.09 running PHP 5.4
    2) 64bit Amazon Linux 2013.09 running PHP 5.4
    ...
    19) 32bit Amazon Linux 2013.09 running Python 2.7
    ...
    27) 32bit Amazon Linux 2013.09 running Ruby 1.9.3
    28) 64bit Amazon Linux 2013.09 running Ruby 1.9.3
    Select (1 to 28): 19



Now we need to specify an environment type.  
Either choice is okay here, but we've selected the LoadBalanced environment in case our enrollment is very popular.  
A LoadBalanced environment will spin up extra machines if we need them.

    Select an environment type.
    Available environment types are:
    1) LoadBalanced
    2) SingleInstance
    Select (1 to 2): 1



The next selection is asking us if we would like to create a database, we select "y" as our application will require one.  
We'll create a fresh database instance from **[No snapshot]** (Option 1).

    Create an RDS DB Instance? [y/n]: y
    Create an RDS BD Instance from (current value is "[No snapshot]"):
    1) [No snapshot]
    2) [Other snapshot]
    Select (1 to 2): 1



Enter a password to use for your database instance.
    
    Enter an RDS DB master password: 
    Retype password to confirm: 


In order to preserve our database if we terminate the enviroment, we'll create snapshots.

    If you terminate your environment, your RDS DB Instance will be deleted and you will lose your data.
    Create snapshot? [y/n]: y


Now we'll create a default instance profile.

    Attach an instance profile (current value is "[Create a default instance profile]"):
    1) [Create a default instance profile]
    2) aws-elasticbeanstalk-ec2-role
    3) [Other instance profile]
    Select (1 to 3): 1
    Updated AWS Credential file at "/home/yourusername/.elasticbeanstalk/aws_credential_file".



Once complete you can start your application.

    [yourusername@yourmachine django_study_enrollment]$ eb start
    

After a few minutes your application is running and a URL is output.  

Monitoring of progress can also be done at the AWS web interface [https://console.aws.amazon.com/elasticbeanstalk/](https://console.aws.amazon.com/elasticbeanstalk/)

Status may also be monitored using the eb status command

    eb status --verbose

From here you can update your project and commit as usual with git.  To update the application you can push your git commits to your application directly from the command line.

    git commit
    git aws.push

To stop your application, use the online dashboard or the eb tool to stop.

    eb stop

Configuration
-------------

Django's admin interface is used to configure the various aspects of enrollment.

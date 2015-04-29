# Galaxy

Providing a command line interface for galaxy platform users to perform data analysis with either separate tools or workflows.

For information about the Galaxy platform: http://galaxyproject.org/

Usage:

	connect2galaxy.py

  Access to any galaxy platform as long as you have the url. It could be your local galaxy, server galaxy from your organization or the public galaxy at http://usegalaxy.org/
  
  Two ways to connect:
  
  Use account info:
  
  	python connect2galaxy.py -u localhost:8080 -e you@email.com -p password
  
  Use API-key assigned by administrator:
  
  	python connect2galaxy.py -u localhost:8080 -k your_API_key
  

Update log:

	04/10/2015 connect2galaxy.py
	04/13/2015 Tab2VCF A tool to convert tabular format to VCF file, with Galaxy wrapper scripted.

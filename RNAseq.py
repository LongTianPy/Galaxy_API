<<<<<<< HEAD
 #! /usr/bin/python
"""This script uses Galaxy API 'bioblend' to access galaxy instance with url and account info or API key. It aims to realize performing data analysis by visiting workflow stored in galaxy instance from command line."""
"""Despite of this, it still needs galaxy server running."""

###IMPORT###
from bioblend import galaxy
import optparse
import uuid




###FUNCTION###
def connect_to_galaxy():
	"""
		Connect to galaxy instance by options of url, email, password, API key.
		Note that if user has typed API key, email and password are not required.
		And if no API input, email and password should be indicated.
		"""

    GI = galaxy.GalaxyInstance(url="localhost:8080",key="2b55a6c05d88b92aff00b3a58c8cc409")

	try:
		GI.histories.get_histories()
		return GI
	except:
		print "Please make sure Galaxy is running."
def run_workflow(GI):
    history = GI.histories.create_history(str(uuid.uuid4()))
    workflow = GI.workflows.show_workflow('f2db41e1fa331b3e')
    library = GI.libraries.create_library(str(uuid.uuid4()))
    upload_lib = GI.libraries.upload_file_from_server(library['id'],server_dir='.') # No subfolders in library_import
    
    inputs={}
    for i in upload_lib:
        if i['name'][-2:] == 'fa':
            reference_genome_id = i['id']
        elif i['name'][-3:] == 'gtf':
            reference_annotation_id = i['id']
        else:
            inputs[i['name']]=i['id']
    inputnames = inputs.keys()
    inputnames = sorted(inputnames)
    datamap = {'127':{'src':'ld','id':inputs[inputnames[0]]},
              '128':{'src':'ld','id':inputs[inputnames[1]]},
              '129':{'src':'ld','id':inputs[inputnames[2]]},
              '130':{'src':'ld','id':inputs[inputnames[3]]},
              '132':{'src':'ld','id':reference_annotation_id},
              '131':{'src':'ld','id':reference_genome_id}
              }

    output = GI.workflows.run_workflow(workflow_id='f2db41e1fa331b3e',dataset_map=datamap,history_id=history['id'])
    for i in output['outputs']:
        GI.datasets.download_dataset(i,file_path='/home/outputs')


###MAIN###
if __name__ == '__main__':

    GI = connect_to_galaxy(url,email,password,API_key)
    run_workflow(GI)



=======
#! /usr/bin/python
"""This script uses Galaxy API 'bioblend' to access galaxy instance with url and account info or API key. It aims to realize performing data analysis by visiting workflow stored in galaxy instance from command line."""
"""Despite of this, it still needs galaxy server running."""

###IMPORT###
from bioblend import galaxy
import optparse
import uuid #for unique history id




###FUNCTION###
def connect_to_galaxy(url,email,password,API_key):
	"""
		Connect to galaxy instance by options of url, email, password, API key.
		Note that if user has typed API key, email and password are not required.
		And if no API input, email and password should be indicated.
		"""
	url = url
	if API_key:
		GI = galaxy.GalaxyInstance(url,API_key)
	else:
		GI = galaxy.GalaxyInstance(url,email=email, password=password)
	try:
		GI.histories.get_histories()
		return GI
	except:
		print "Please make sure your email & password or API key is correct."
def run_workflow(GI):
    history = GI.histories.create_history(str(uuid.uuid4())) # Create a history with unique id
    workflow = GI.workflows.show_workflow('4f17b35d7b60af16')
    path = '/Users/longtian/Desktop/RNAseq/'
    input1 = GI.tools.upload_file(path+'adrenal_1.fastq',history['id'],type='txt') # Upload files to history
    input2 = GI.tools.upload_file(path+'adrenal_2.fastq',history['id'],type='txt')
    input3 = GI.tools.upload_file(path+'brain_1.fastq',history['id'],type='txt')
    input4 = GI.tools.upload_file(path+'brain_2.fastq',history['id'],type='txt')
    reference_genome = GI.tools.upload_file(path+'chr19.fa',history['id'],type='txt')
    reference_annotation = GI.tools.upload_file(path+'chr19.gtf',history['id'],type='txt')
    datamap = {'1691569':{'src':'hda','id':input1['outputs'][0]['id']}, #Input should be in dictionary object. The numbers at the beginning is the id of input
              '1691570':{'src':'hda','id':input2['outputs'][0]['id']},
              '1691571':{'src':'hda','id':input3['outputs'][0]['id']},
              '1691572':{'src':'hda','id':input4['outputs'][0]['id']},
              '1691574':{'src':'hda','id':reference_annotation['outputs'][0]['id']},
              '1691573':{'src':'hda','id':reference_genome['outputs'][0]['id']}
              }

    output = GI.workflows.run_workflow(workflow_id='4f17b35d7b60af16',dataset_map=datamap,history_id=history['id']) #Run this workflow



###MAIN###
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-u', dest = 'url', default='localhost:8080', help = 'Galaxy instance to connect, including port if there is one.')
    parser.add_option('-e', dest = 'email', default= '', help = 'Email address used to login to the galaxy platform.')
    parser.add_option('-p', dest = 'password', default = '', help = 'Password.')
    parser.add_option('-k', dest = 'API_key', default = '', help =  "API key generated by admin, use email and password if you do not have one or contact the admin.")

    (options,args) = parser.parse_args()
    url = options.url
    email = options.email
    password = options.password
    API_key = options.API_key

    GI = connect_to_galaxy(url,email,password,API_key)
    run_workflow(GI)



>>>>>>> origin/master

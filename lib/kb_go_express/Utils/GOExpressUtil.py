import time
import json
import os
import uuid
import errno
import subprocess
import zipfile
import shutil
import csv
import numpy
import fileinput
import re

from DataFileUtil.DataFileUtilClient import DataFileUtil
from KBaseReport.KBaseReportClient import KBaseReport
from GenomeSearchUtil.GenomeSearchUtilClient import GenomeSearchUtil
#from biokbase.workspace.client import Workspace as Workspace
from Workspace.WorkspaceClient import Workspace as Workspace


#from biokbase.workspace.client import Workspace


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))



class GOExpressUtil:

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def _expression_object_to_tsv(self, expression_object, expression_matrix_TSV_path):
    

                log ('Starting get_expression_matrix')
       
                expression_matrix_data = self.df.get_objects({'object_refs':
                                                  [expression_object]})['data'][0]['data']
                #print expression_matrix_data

                expression_matrix_TSV = []
                col_ids = expression_matrix_data['data']['col_ids']
                ids =  "\t". join ([str(x) for x in col_ids])
                
                expression_matrix_TSV.append(" " + "\t" + ids + "\n")

                feature_list = expression_matrix_data['data']['row_ids']
                values = expression_matrix_data['data']['values']

                for feature, value in zip (feature_list, values):
                    row_value =  "\t".join(map(str, value)) 
                    expression_matrix_TSV.append (feature + "\t" + row_value + "\n")


                textstring_TSV = "".join (expression_matrix_TSV)
                #TODO put some try and catch here
                file = open(expression_matrix_TSV_path,'w')  
                file.write(textstring_TSV)
                file.close()

                return expression_matrix_TSV_path



    def _get_go_maps_from_genome(self, genome_ref):
        
        log('start parsing GO terms from genome')

        feature_num = self.gsu.search({'ref': genome_ref})['num_found']

        genome_features = self.gsu.search({'ref': genome_ref,
                                               'limit': feature_num,
                                               'sort_by': [['feature_id', True]]})['features']

        feature_id_go_id_list_map = {}
        go_id_feature_id_list_map = {}
        go_id_go_term_map = {}
        feature_id_feature_info_map = {}

        for genome_feature in genome_features:
                feature_id = genome_feature.get('feature_id')
                feature_func = genome_feature.get('function')
                feature_type = genome_feature.get('feature_type')
                ontology_terms = genome_feature.get('ontology_terms')
                #print "ontology"
                #print ontology_terms

                #print ('{}\t{}\t{}'.format(feature_id, feature_func , feature_type))



                #feature_id_feature_info_map.update({feature_id: {'function': feature_func,
                 #                                                'feature_type': feature_type}})

                go_id_list = []
                if ontology_terms:
                    for ontology_id, ontology_term in ontology_terms.iteritems():
                        if re.match('[gG][oO]\:.*', ontology_id):
                            go_id_go_term_map.update({ontology_id: ontology_term})
                            go_id_list.append(ontology_id)

                if go_id_list:
                    feature_id_go_id_list_map.update({feature_id: go_id_list})

                    for go_id in go_id_list:
                        if go_id in go_id_feature_id_list_map:
                            feature_ids = go_id_feature_id_list_map.get(go_id)
                            feature_ids.append(feature_id)
                            go_id_feature_id_list_map.update({go_id: feature_ids})
                        else:
                            go_id_feature_id_list_map.update({go_id: [feature_id]})
                else:
                    if not re.match('.*\.\d*', feature_id):
                        feature_id_go_id_list_map.update({feature_id: 'Unlabeled'})
        return (feature_id_go_id_list_map, go_id_feature_id_list_map,
                go_id_go_term_map, genome_features)




    def _get_ontology_hash(self):
        ontology_hash = dict()
        ontologies = self.ws.get_objects([{'workspace': 'KBaseOntology',
                                           'name': 'gene_ontology'},
                                          {'workspace': 'KBaseOntology',
                                           'name': 'plant_ontology'}])
        ontology_hash.update(ontologies[0]['data']['term_hash'])
        ontology_hash.update(ontologies[1]['data']['term_hash'])

        return ontology_hash

    def _generate_supporting_files(self, result_directory,  
                                   feature_id_go_id_list_map, genome_ref,
                                    genome_features, ontology_hash):
                 
        supporting_files = list()

        feature_id_go_ids_map_file = os.path.join(result_directory, 'feature_id_go_ids_map.txt')
        go_id_description_file = os.path.join(result_directory, 'go_id_description.txt')
        feature_ids_file = os.path.join(result_directory, 'feature_ids_description.txt')
        genome_info_file = os.path.join(result_directory, 'genome_info.txt')
       

        supporting_files.append(feature_id_go_ids_map_file)
        supporting_files.append(go_id_description_file)
        supporting_files.append(feature_ids_file)
        supporting_files.append(genome_info_file)
       
        total_feature_ids = feature_id_go_id_list_map.keys()
        feature_ids_with_feature = []
        for feature_id, go_ids in feature_id_go_id_list_map.iteritems():
            if isinstance(go_ids, list):
                    feature_ids_with_feature.append(feature_id)
        genome_name = self.ws.get_object_info3({'objects': 
                                                    [{'ref': genome_ref}]})['infos'][0][1]

        print genome_info_file
        with open(genome_info_file, 'wb') as genome_info_file:
                genome_info_file.write('genome_name: {}\n'.format(genome_name))
                genome_info_file.write('features: {}\n'.format(len(total_feature_ids)))
                genome_info_file.write('features with term: {}'.format(len(feature_ids_with_feature)))


       
        with open(feature_id_go_ids_map_file, 'wb') as feature_id_go_ids_map_file:
            with open(go_id_description_file, 'wb') as go_id_description_file:

                feature_id_go_ids_map_file.write('{}\t{}\n'.format("gene_id", "go_id"))
                go_id_description_file.write('{}\t{}\t{}\n'.format("go_id","name", "namespace")) 
                                                                        
                for feature_id, go_ids in feature_id_go_id_list_map.iteritems():
                    if isinstance(go_ids, str):
                        feature_id_go_ids_map_file.write('{}\t{}\n'.format(feature_id, 
                                                                            go_ids))
                        ontology_name = ontology_hash.get(go_ids).get('name')
                        ontology_namespace = ontology_hash.get(go_ids).get('namespace')
                        go_id_description_file.write('{}\t{}\t{}\n'.format(go_ids, 
                                                                        ontology_name, 
                                                                        ontology_namespace))
                    else:
                        for go_id in go_ids: 
                            feature_id_go_ids_map_file.write('{}\t{}\n'.format(feature_id, 
                                                                                go_id))
                            ontology_name = ontology_hash.get(go_id).get('name')
                            ontology_namespace = ontology_hash.get(go_id).get('namespace')
                            go_id_description_file.write('{}\t{}\t{}\n'.format(go_id, 
                                                                        ontology_name, 
                                                                        ontology_namespace))

                        

        with open(feature_ids_file, 'wb') as feature_ids_file:
            feature_ids_file.write('{}\t{}\n'.format("gene_id", "description"))

            for genome_feature in genome_features:
                feature_id = genome_feature.get('feature_id')
                feature_func = genome_feature.get('function')
                feature_type = genome_feature.get('feature_type')
                ontology_terms = genome_feature.get('ontology_terms')

                if ontology_terms:
                    feature_ids_file.write('{}\t{}\n'.format(feature_id, feature_func))


        result_file = os.path.join(result_directory, 'supporting_files.zip')
        with zipfile.ZipFile(result_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
            for supporting_file in supporting_files:
                 zip_file.write(supporting_file, 
                               os.path.basename(supporting_file))

        return [{'path': result_file,
                      'name': os.path.basename(result_file),
                      'label': os.path.basename(result_file),
                      'description': 'GOexpress supporting files'}]




    # def _run_command(self, command):
    #     """
    #     _run_command: run command and print result
    #     """
    #         log('Start executing command:\n{}'.format(command))
    #         pipe = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #         output = pipe.communicate()[0]
    #         exitCode = pipe.returncode

    #         if (exitCode == 0):
    #             log('Executed commend:\n{}\n'.format(command) +
    #                 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output))
    #         else:
    #             error_msg = 'Error running commend:\n{}\n'.format(command)
    #             error_msg += 'Exit Code: {}\nOutput:\n{}'.format(exitCode, output)
    #             raise ValueError(error_msg)


    def __init__(self, config):
            self.ws_url = config["workspace-url"]
            self.callback_url = config['SDK_CALLBACK_URL']
            self.token = config['KB_AUTH_TOKEN']
            self.shock_url = config['shock-url']
            self.df = DataFileUtil(self.callback_url)
            self.gsu = GenomeSearchUtil(self.callback_url)
            self.ws = Workspace(self.ws_url, token=self.token)
            self.scratch = config['scratch']


    def run_goexpress_app(self, params):

        result_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(result_directory)


        (feature_id_go_id_list_map, 
             go_id_feature_id_list_map,
             go_id_go_term_map, 
             genome_features) = self._get_go_maps_from_genome(params['genome_ref'])

        
        ontology_hash = self._get_ontology_hash()

        
        output = self._generate_supporting_files(result_directory, 
                                                feature_id_go_id_list_map, 
                                                params['genome_ref'],
                                                genome_features, ontology_hash)

    

 




        #expression_matrix_file = self._expression_object_to_tsv(params['expression_ref'],
        #                                                        expression_matrix_file)

       # condition_sample_relationship_file = self._write_condition_sample_relationship(params['sample_n_conditions'],
         #                                                                             condition_sample_relationship_file)
        #gene_ontology_data = 



            


        





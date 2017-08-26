# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import json
from kb_go_express.Utils.GOExpressUtil import GOExpressUtil

#END_HEADER


class kb_go_express:
    '''
    Module Name:
    kb_go_express

    Module Description:
    A KBase module: kb_go_express
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "git@github.com:pranjan77/kb_go_express.git"
    GIT_COMMIT_HASH = "c92316728321c79a9eefbf20a7a832c37755107b"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        #END_CONSTRUCTOR
        pass


    def run_goexpress_app(self, ctx, params):
        """
        run_goexpress_app
        ref: https://bioconductor.org/packages/release/bioc/html/GOexpress.html
        :param params: instance of type "GOExpressInput" (required params:
           workspace_name: Name of the workspace expressionset_ref:
           ExpressionSet object reference condition1: First condition
           condition2: Second condition Number of permutations:
           num_permutations optional params:) -> structure: parameter
           "workspace_name" of String, parameter "expression_ref" of type
           "obj_ref" (Reference), parameter "genome_ref" of type "obj_ref"
           (Reference), parameter "sample_id1" of list of String, parameter
           "sample_n_conditions" of list of mapping from String to String,
           parameter "num_permutations" of Long, parameter
           "fold_change_cutoff" of Double
        :returns: instance of type "GOExpressResult" (result_directory:
           folder path that holds all files generated by run_goexpress_app
           report_name: report name generated by KBaseReport report_ref:
           report reference generated by KBaseReport) -> structure: parameter
           "result_directory" of String, parameter "report_name" of String,
           parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN run_goexpress_app
        #x=ExpressionUtils()

        print "printing params"
        print json.dumps(params)

        go_express_runner = GOExpressUtil(self.config)
        returnVal = go_express_runner.run_goexpress_app(params)


        returnVal={}



        #END run_goexpress_app

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method run_goexpress_app return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]

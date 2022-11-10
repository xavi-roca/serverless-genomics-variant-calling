"""

REMAINING THINGS TO DO:
-Implement new fasta partitioner
-Add s3 fastq location
-Improve/Remake log system
-Add the dockerfile folder
-More refactoring

"""

import argparse
from varcall_arguments import Arguments
from pipeline_caller import PipelineCaller

 
if __name__ == "__main__":
    ###################################################################
    #### COMMAND LINE ARGUMENTS
    ###################################################################
    parser = argparse.ArgumentParser(description='Variant Caller - Cloudbutton Genomics Use Case demo')

    ###################################################################
    #### COMMAND-LINE ARGUMENTS
    ###################################################################
    # File Names And Locations
    # fastq in SRA database
    parser.add_argument('-fq','--fq_seqname', help='Fastq sequence name (for example SRR6052133) used for SRA database',required=False)
    # fastq in s3 bucket
    parser.add_argument('-fq1','--fastq1', help='Fastq file 1, stored in s3',required=False)
    parser.add_argument('-fq2','--fastq2', help='Fastq file 2, stored in s3 (paired end sequencing) - optional',required=False)
    parser.add_argument('-fa','--fasta_file',help='Fasta reference filename', required=True)
    # input files locations
    parser.add_argument('-cl','--cloud_adr',help='cloud provider url prefix', required=False)
    parser.add_argument('-b','--bucket',help='cloud provider bucket name', required=True)
    parser.add_argument('-fb','--fasta_bucket',help='cloud provider bucket name - for fasta file', required=False)
    # fastq data source (SRA or s3)
    parser.add_argument('-ds','--datasource',help='Data source', required=False)

    # File Splitting Parameters
    parser.add_argument('-nfq','--fastq_read_n', help='Number of reads per fastq chunk ',required=False)
    parser.add_argument('-nfa','--fasta_workers',help='Number of workers', required=True)

    # Pipeline-Specific Parameters
    parser.add_argument('-t','--tolerance',help='number of additional strata to include in filtration of map file', required=False)
    parser.add_argument('-ff','--file_format',help='mpileup file format - csv or parquet', required=False)

    # Run Settings
    parser.add_argument('-itn','--iterdata_n',help='Number of iterdata elements to run', required=False)
    parser.add_argument('-cf','--concur_fun',help='concurrent function quota limit', required=False)
    parser.add_argument('-s3w','--temp_to_s3',help='Write intermediate temp files to s3 for debugging', required=False)
    parser.add_argument('-rt','--runtime_id',help='runtime to use to execute the map-reduce', required=False)
    parser.add_argument('-rtm','--runtime_mem',help='runtime memory to be assigned to each function - maximum 2048 MB', required=False)
    parser.add_argument('-rtr','--runtime_mem_r',help='runtime memory to be assigned to reduce function - maximum 10240 MB', required=False)
    parser.add_argument('-rts','--runtime_storage',help='runtime storage to be assigned to map function - maximum 10000 MB - currently set manually', required=False)
    parser.add_argument('-bs','--buffer_size',help='memory in percentatge for buffer size - maximum 100%', required=False)
    parser.add_argument('-ftm','--func_timeout_map',help='timeout for map function - maximum 900', required=False)
    parser.add_argument('-ftr','--func_timeout_reduce',help='timeout for reduce function - maximum 900', required=False)
    parser.add_argument('-sk','--skip_map',help='True/False; use mpileups generated by previous run, to run only reducer', required=False)
    parser.add_argument('-lb','--loadbalancer',help='load balancer execution method: manual|select', required=False)
    
    
    ###################################################################
    #### PARSE COMMAND LINE ARGUMENTS
    ###################################################################
    args = parser.parse_args()
    params = {k: v for k, v in vars(args).items() if v is not None}
    
    if args.fasta_bucket is None:
        params['fasta_bucket'] = args.bucket
        
    params['fastq_chunk_size'] = 4*int(args.fastq_read_n)
    
    if args.fastq2 is None:
        params['seq_type'] = "single-end"
    else:
        params['seq_type'] = "paired-end"

    arguments = Arguments(**params)
    
    ###################################################################
    #### EXECUTE PIPELINE
    ###################################################################
    pipeline = PipelineCaller()
    pipeline.execute_pipeline(arguments)

#! /usr/bin/python
"""This is used for converting tab-delimited file to VCF file."""

#IMPORT
import os,optparse

#CLASS


#FUNCTIONS
def header_collection(header = None, sample_names= None):
	if not header:
		header = {}
	if not header.has_key('fileformat'):
		header['fileformat'] = 'VCFv4.0'
	if not header.has_key('source'):
		header['source'] = "Galaxy"
	if not header.has_key('HEADER'):
		header['HEADER'] = """CHROM\tPOS\tREF\tALT\tINFO\tFORMAT\tSAMPLE"""
	txt = """##INFO=<ID=ADP,Number=1,Type=Integer,Description="Average per-sample depth of bases with Phred score >= 15">\n##INFO=<ID=WT,Number=1,Type=Integer,Description="Number of samples called reference (wild-type)">\n##INFO=<ID=HET,Number=1,Type=Integer,Description="Number of samples called heterozygous-variant">\n##INFO=<ID=HOM,Number=1,Type=Integer,Description="Number of samples called homozygous-variant">\n##INFO=<ID=NC,Number=1,Type=Integer,Description="Number of samples not called">\n##FILTER=<ID=str10,Description="Less than 10% or more than 90% of variant supporting reads on one strand">\n##FILTER=<ID=indelError,Description="Likely artifact due to indel reads at this position">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">\n##FORMAT=<ID=SDP,Number=1,Type=Integer,Description="Raw Read Depth as reported by SAMtools">\n##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Quality Read Depth of bases with Phred score >= 15">\n##FORMAT=<ID=RD,Number=1,Type=Integer,Description="Depth of reference-supporting bases (reads1)">\n##FORMAT=<ID=AD,Number=1,Type=Integer,Description="Depth of variant-supporting bases (reads2)">\n##FORMAT=<ID=FREQ,Number=1,Type=String,Description="Variant allele frequency">\n##FORMAT=<ID=PVAL,Number=1,Type=String,Description="P-value from Fisher's Exact Test">\n##FORMAT=<ID=RBQ,Number=1,Type=Integer,Description="Average quality of reference-supporting bases (qual1)">\n##FORMAT=<ID=ABQ,Number=1,Type=Integer,Description="Average quality of variant-supporting bases (qual2)">\n##FORMAT=<ID=RDF,Number=1,Type=Integer,Description="Depth of reference-supporting bases on forward strand (reads1plus)">\n##FORMAT=<ID=RDR,Number=1,Type=Integer,Description="Depth of reference-supporting bases on reverse strand (reads1minus)">\n##FORMAT=<ID=ADF,Number=1,Type=Integer,Description="Depth of variant-supporting bases on forward strand (reads2plus)">\n##FORMAT=<ID=ADR,Number=1,Type=Integer,Description="Depth of variant-supporting bases on reverse strand (reads2minus)">\n"""
	header_str = """##fileformat=%s\n##source=%s\n%s#%s"""%(header['fileformat'],header['source'],txt,header['HEADER'])

	return header, header_str

def convert(input,output):
	header, header_str = header_collection(None, input)

	f = open(input,'r')
	lines = [i.split('\t') for i in f.readlines()[1:]]
	f = open(input,'r')
	headerline=f.readlines()[0].split('\t')
	headerline[-1]=headerline[-1][:-1]
	f.close()
	input_dict = {}
	input_dict[headerline[0]] = [i[0] for i in lines]
	input_dict[headerline[1]] = [i[1] for i in lines]
	input_dict[headerline[2]] = [i[2] for i in lines]
	input_dict[headerline[3]] = [i[3] for i in lines]
	input_dict[headerline[4]] = [i[4] for i in lines]
	input_dict[headerline[5]] = [i[5] for i in lines]
	input_dict[headerline[6]] = [i[6] for i in lines]
	input_dict[headerline[7]] = [i[7] for i in lines]
	input_dict[headerline[8]] = [i[8] for i in lines]
	input_dict[headerline[9]] = [i[9] for i in lines]
	input_dict[headerline[10]] = [i[10] for i in lines]
	input_dict[headerline[11]] = [i[11][:-1] for i in lines]
	output_file = open(output, 'w')

	output_file.write(header_str+'\n')
	for i in range(len(lines)):
		sample_list = [input_dict['RD'][i],input_dict['AD'][i],input_dict['FREQ'][i],input_dict['GT'][i],input_dict['RDF'][i],input_dict['RDR'][i],
						input_dict['ADF'][i],input_dict['ADR'][i],]
		sample_str = ':'.join(sample_list)
		line = [input_dict['CHROM'][i],input_dict['POS'][i],input_dict['REF'][i],input_dict['ALT'][i],
						'RD:AD:FREQ:GT:RDF:RDR:ADF:ADR',sample_str]
		line_str = '\t'.join(line)+'\n'
		output_file.writelines(line_str)
	output_file.close()

if __name__ == '__main__':
	parser = optparse.OptionParser()

	parser.add_option('-i', dest = 'input', default = '', help='Path of the input file')
	parser.add_option('-o', dest = 'output', default = '', help = 'path of the output file')

	(options,args) = parser.parse_args()

	input = options.input
	output = options.output

	header_collection()
	convert(input,output)


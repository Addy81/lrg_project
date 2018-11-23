



import xml.etree.ElementTree as ET

tree = ET.parse('LRG_384.xml')
root = tree.getroot()


for child in root:
	print(child.tag, child.attrib)


class lrgobject:
	def __init__(self, lrg_id, hgnc_id, seq_source, mol_type):
		self.lrg_id = lrg_id
		self.hgnc_id = hgnc_id
		self.seq_source = seq_source
		self.mol_type = mol_type




lrg_id = root.find('fixed_annotation/id').text
hgnc_id = root.find('fixed_annotation/hgnc_id').text
seq_source = root.find('fixed_annotation/sequence_source').text
mol_type = root.find('fixed_annotation/mol_type').text



newlrgobj = lrgobject(lrg_id, hgnc_id, seq_source, mol_type)




print(newlrgobj.lrg_id)


'''
requirements
code that functions
whats the level of documentation
readme
documentation in code
tests in code
ISO requirements
verified examples
testset data
'''
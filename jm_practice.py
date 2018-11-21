



import xml.etree.ElementTree as ET

tree = ET.parse('LRG_384.xml')
root = tree.getroot()


for child in root:
	print(child.tag, child.attrib)


id = root.find('fixed_annotation/hgnc_id')
print(id.text)
#print(root['fixed_annotation'])
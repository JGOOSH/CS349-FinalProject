import os
from collections import OrderedDict 
import spacy

def set_log_permission(file, permission):
	permission = permission.lower()
	code = None
	if permission in ['owner', 'owner_read', 'owner read']:
		code = stat.S_IREAD
	elif permission in ['group', 'group_read', 'group read']:
		code = stat.S_IRGRP 
	elif permission in ['others', 'other_read', 'other read']:
		code = stat.S_IROTH
	else:
		raise ValueError("Unaccepted permission code")
	os.chmod(file, permission)

def close_log_w_permission(file, permission):
	f = file.name
	file.close()
	set_log_permission(f, permission)

def parse(log):
	pair_dict = OrderedDict()
	for pair in log.strip().split(", "):
		key, value = pair.split("=")
		pair_dict[key] = value
	return pair_dict

def log_validate(log):
	f = open(log)
	log_txt = f.read()
	print("Input Log:", log_txt)
	parsed = parse(log_txt)
	print("Parsed pairs:",str(parsed))
	print("Type numbers that you want to exclude from the log")
	print("Separate by space and press Enter if none")
	idx = 0
	for key, value in parsed.items():
		print(str(idx) +":", key, "=", value) 
		idx += 1
	inp = input("Enter the number(s): ")
	indices = list()
	for i in str(inp).strip().split(" "):
		if i.isdigit():
			indices.append(int(i))
		else:
			raise ValueError("Unaccepted value")
	modified_log = ''
	for idx in range(len(parsed)):
		if idx in indices:
			continue
		elif idx >= 0 and idx < len(parsed):
			item = list(parsed.items())[idx]
			modified_log += item[0] + "=" + item[1]
			modified_log += ", "
	print("Output Log:", modified_log[:-4])	
	if modified_log == '':
		return modified_log
	return modified_log[:-4]

import pprint
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()

def log_NER(log):
	f = open(log)
	text = f.read().strip()
	print("Input Log:", text)
	doc = nlp(text)
	if (len(doc.ents) == 0 ):
		print("Could not find any entities")
		return None
	print("Type numbers that you want to exclude from the log")
	print("Separate by space and press Enter if none")
	idx = 0
	for ent in doc.ents:
		print(str(idx) +":", ent.text, ",", ent.label_)
		idx += 1
	inp = input("Enter the number(s): ")
	indices = list()
	for i in str(inp).strip().split(" "):
		if i.isdigit():
			indices.append(int(i))
		else:
			raise ValueError("Unaccepted value")
	for idx in range(len(doc.ents)):
		if idx not in indices:
			continue
		elif idx >= 0 and idx < len(doc.ents):
			ent = doc.ents[idx]
			replace = ''.join('*' for i in range(len(ent.text)))
			text = text[:ent.start_char-1] + replace + text[ent.end_char:]
	print("Output Log:", text)
	return text
	

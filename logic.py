import requests
from config import magic_1, magic_2, counter_file, users_file

# сделать класс PMID, в котором будут лежать все функции по его обработке
# нестандартные случаи обрабатывать через отнаследованный класс PMID

def get_raw_text(pmid):
	"""Создает ссылку по PMID и получает неотформатированную аннотацию"""
	link = magic_1 + pmid + magic_2
	r = requests.get(link)
	raw_text = str(r.text.encode().decode('unicode-escape'))
	return raw_text

def get_classic_nlm(pmids): # done
	"""Создает отформатированную аннотацию NLM."""
	references = []
	count = False
	for pmid in pmids:
		try:
			raw_text = get_raw_text(pmid)
			start_reference = raw_text.index('"nlm"') + 17
			temp_end_reference = raw_text.index('"format"', start_reference) - 3
			end_reference = raw_text.index('PMID', start_reference, temp_end_reference) - 1
			reference = raw_text[start_reference:end_reference]
			count = get_count()
		except ValueError:
			reference = f"No citations data found for article {pmid}!"
		references.append(reference)
	reference = upload(references)
	return reference, count



def upload(references):
	reference = ''
	for _ in references:
		reference += f"{_}\n\n"
	return reference

def get_count():
	with open(counter_file, 'r') as f:
		count = f.read()
		count = int(count)
		count += 1
		count = str(count)
		update_count(count)
		return count

def update_count(count):
	with open(counter_file, 'w') as f:
		f.write(str(count))

def write_user_id(id):
	with open(users_file, 'a') as f:
		f.write(id)
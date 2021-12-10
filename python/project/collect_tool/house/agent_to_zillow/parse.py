from bs4 import BeautifulSoup
import re
import requests
import time

def extract_price_from_zillow(house_soup, house):
	house['Price'] = house_soup.find('div', {'class': 'ds-summary-row'}).span.span.span.text

def extract_bed_bath_from_zillow(house_soup, house):
	bed_bath = house_soup.find(text='Bedrooms and bathrooms')
	for b in bed_bath.parent.parent.find_all('li'):
		key, value = b.text.split(':')
		house[key.strip()] = value.strip()

def extrat_facts_from_zillow(house_soup, house):
	facts = house_soup.find('ul', {'class': 'ds-home-fact-list'}).find_all('li')
	for fact in facts:
		key, value = fact.find_all('span')
		house[key.text.strip()] = value.text.strip()

def extrat_school_from_zillow(house_soup, house):
	school_area = house_soup.find('ul', {'id': 'ds-nearby-schools-list'})
	schools = school_area.find_all('li')
	for idx, s in enumerate(schools):
		s_score, s_detail = s.findChildren("div", recursive=False)
		score_area = s_score.div.find_all('span')
		if len(score_area) < 2:
			break
		score = score_area[0].text + score_area[1].text
		grade = s_detail.div.text
		name = s_detail.a.text
		house['School ' + str(idx+1)] = '{} - {} ({})'.format(score, grade, name)

def parse_data_from_agent(file_path):
	houses_raw = {}
	with open(file_path, 'r', encoding='utf-8') as f:
		content = f.read().encode('utf-8')
		soup = BeautifulSoup(content, "html.parser")
		h_areas = soup.find_all('td', text="Addr:")
		for h in h_areas:
			next_detail_area = h.findNext('tbody').findNext('tbody')
			h_addr = h.findNext('td').text.strip()
			h_town = next_detail_area.find(text='Town:').findNext('td').text
			h_zip = next_detail_area.find(text='Zip:').findNext('td').text
			zillow_str = 'https://www.zillow.com/homes/{addr}-{town},-NJ-{zip}_rb'.format(addr='-'.join(h_addr.split(' ')), town=h_town, zip=h_zip)
			addr_str = '{addr}, {town}, NJ {zip}'.format(addr=h_addr, town=h_town, zip=h_zip)
			houses_raw[addr_str] = zillow_str
	return houses_raw

def generate_excel_file(houses, output_excel_path):
	headers = {};
	for h in houses:
		for key in h.keys():
			if key not in headers:
				headers[key] = True

	buffer = [];
	buffer.append('\t'.join(headers))
	for h in houses:
		tmpData = [];
		for key in headers:
			if key in h:
				tmpData.append(h[key])
			else:
				tmpData.append('')
		buffer.append('\t'.join(tmpData))

	with open(output_excel_path, 'w', encoding='utf-8') as f:
		f.write('\n'.join(buffer))

def main(agent_file_path, output_excel_path):
	agent_house_raw = parse_data_from_agent(agent_file_path)
	houses = []
	for key, value in agent_house_raw.items():
		print(key)
		header = { "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36" }
		res = requests.get(value,  headers = header)
		extrat_funcs = [
			extract_price_from_zillow, extract_bed_bath_from_zillow, extrat_facts_from_zillow, extrat_school_from_zillow
		]
		soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")
		data = {};
		data['Address'] = key
		data['URL'] = value

		for e in extrat_funcs:
			try:
				e(soup, data)
			except:
				continue

		houses.append(data)
		time.sleep(2)

	generate_excel_file(houses, output_excel_path)

if __name__ == '__main__':
	input_agent_path = 'C:/Users/ganyf/Downloads/sourceNew.html'
	output_excel_path = 'C:/Users/ganyf/Downloads/result.tsv'
	main(input_agent_path, output_excel_path)
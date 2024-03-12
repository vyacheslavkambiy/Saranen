import xml.etree.ElementTree as ET
import json

# Function to parse currency rates from XML
def parse_currency_rates(xml_file):
    currency_rates = {}
    tree = ET.parse(xml_file)
    root = tree.getroot()
    cube = root.find('.//Cube[@time="2015-10-22"]')  # Adjust the XPath expression
    if cube is not None:
        for rate in cube.findall('.//Cube'):
            currency = rate.get('currency')
            value = float(rate.get('rate'))
            currency_rates[currency] = value
    return currency_rates


# Function to convert XML data to JSON
def convert_xml_to_json(xml_file, currency_rates):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    data = []
    for palkka in root.findall('.//palkka'):
        henkilosto_id = palkka.get('henkilöstöid')
        person_name = palkka.find('nimi').text
        monthly_salary = float(palkka.find('kuukausittain').text)
        hire_date = palkka.find('työsuhdealkoi')
        hire_date_value = hire_date.text if hire_date is not None else None
        
        # Convert salary to USD
        salary_usd = monthly_salary / currency_rates.get('USD', 1)
        
        data.append({
            'personName': person_name,
            'salary': {
                'monthly': round(salary_usd, 2)  # Round to 2 decimal places
            },
            'hireDate': hire_date_value
        })
    
    return data

# Read currency rates
currency_rates = parse_currency_rates('Currency rates.xml')

# Convert XML data to JSON
json_data = convert_xml_to_json('salaries.xml', currency_rates)

# Output JSON data to the screen
print(json.dumps(json_data, indent=4))

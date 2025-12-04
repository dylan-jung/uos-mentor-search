import json
import os
import glob

def extract_mentors():
    data_dir = 'data'
    output_file = 'mentors_extracted.json'
    extracted_data = []

    # Get all json files in data directory
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    
    print(f"Found {len(json_files)} JSON files.")

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if 'list' in data and isinstance(data['list'], list):
                    for item in data['list']:
                        mentor_info = {
                            'mentorno': item.get('mentorno'),
                            'departnm': item.get('departnm'),
                            'sex': item.get('sex'),
                            'companynm': item.get('companynm'),
                            'duty': item.get('duty'),
                            'introduce': item.get('introduce'),
                            'actcategory': item.get('actcategory'),
                            'mentorname': item.get('mentorname'),
                            # 'repcateogry': item.get('repcateogry')
                        }
                        extracted_data.append(mentor_info)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully extracted {len(extracted_data)} mentors to {output_file}")

if __name__ == "__main__":
    extract_mentors()

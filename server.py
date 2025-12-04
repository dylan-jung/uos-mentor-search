import http.server
import json
import urllib.parse
import os

PORT = 8000
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Global variable to store joined data
MENTOR_DATA = []

def load_and_join_data():
    global MENTOR_DATA
    print("Loading data...")
    
    try:
        with open(os.path.join(DATA_DIR, 'actcategory.json'), 'r', encoding='utf-8') as f:
            act_category = json.load(f)
        
        with open(os.path.join(DATA_DIR, 'duty.json'), 'r', encoding='utf-8') as f:
            duty_category = json.load(f)
            
        with open(os.path.join(DATA_DIR, 'mentors_extracted.json'), 'r', encoding='utf-8') as f:
            mentors = json.load(f)
            
        joined_mentors = []
        for mentor in mentors:
            # Join duty codes
            duty_codes = mentor.get('duty', '').split(',')
            duty_names = [duty_category.get(code.strip(), code.strip()) for code in duty_codes if code.strip()]
            mentor['duty_names'] = duty_names
            mentor['duty_joined'] = ', '.join(duty_names)
            
            # Join actcategory codes
            act_codes = mentor.get('actcategory', '').split(',')
            act_names = [act_category.get(code.strip(), code.strip()) for code in act_codes if code.strip()]
            mentor['actcategory_names'] = act_names
            mentor['actcategory_joined'] = ', '.join(act_names)
            
            joined_mentors.append(mentor)
            
        MENTOR_DATA = joined_mentors
        print(f"Loaded and joined {len(MENTOR_DATA)} mentors.")
        
    except Exception as e:
        print(f"Error loading data: {e}")

class MentorSearchHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/search':
            query_params = urllib.parse.parse_qs(parsed_path.query)
            query = query_params.get('q', [''])[0].lower()
            
            results = []
            if query:
                for mentor in MENTOR_DATA:
                    # Search in relevant fields including name
                    searchable_text = f"{mentor.get('mentorname', '')} {mentor.get('companynm', '')} {mentor.get('departnm', '')} {mentor.get('introduce', '')} {mentor.get('duty_joined', '')} {mentor.get('actcategory_joined', '')}".lower()
                    
                    if query in searchable_text:
                        results.append(mentor)
            else:
                results = MENTOR_DATA
                
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(results, ensure_ascii=False).encode('utf-8'))
            return
            
        return super().do_GET()

if __name__ == "__main__":
    load_and_join_data()
    with http.server.ThreadingHTTPServer(("", PORT), MentorSearchHandler) as httpd:
        print(f"Serving at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

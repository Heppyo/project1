pip install openai
from openai import OpenAI
import csv
import time
import re

# Initialize the OpenAI client
client = OpenAI(api_key='api_key_here')

def construct_prompt(job_listing):
    # The prompt remains the same as in your original code
    prompt = f"""Analyser følgende jobbannonse for "blomsterspråk" og gi en score basert på følgende kriterier:

SCORINGSKRITERIER:
1. Overdreven beskrivelse av jobben (0-10):
   - Score 0-3: Minimal utsmykning
   - Score 4-7: Moderat blomsterspråk
   - Score 8-10: Betydelig overdrivelse

2. Overdådig beskrivelse av arbeidsplassen (0-10):
   - Score 0-3: Direkte beskrivelse
   - Score 4-7: Noe utsmykning
   - Score 8-10: Meget overdreven

3. De 7 mest superlative ordene (I svaret skriv alltid på formated: Kriterium 3: ord1, ord2, ord3, ord4, ord5, ord6, ord7)

SVARFORMAT:
1. Kort analyse (maks 50 ord)
2. Kriterium 1: Score X/10
3. Kriterium 2: Score X/10
4. Kriterium 3: ord1, ord2, ord3, ord4, ord5, ord6, ord7

Jobbannonse:
{job_listing}
"""
    return prompt

def query_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # model specification
            messages=[
                {"role": "system", "content": "You are an AI trained to analyze job listings for excessive language use."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_scores(analysis):
    # Extract scores for criteria 1 and 2
    criteria1_match = re.search(r"Kriterium 1: Score (\d+)/10", analysis)
    criteria2_match = re.search(r"Kriterium 2: Score (\d+)/10", analysis)
    
    # More flexible pattern for criterion 3
    criteria3_pattern = r"Kriterium 3:\s*[\"']?(.*?)[\"']?(?=\n|$|\.|Kriterium)"
    criteria3_match = re.search(criteria3_pattern, analysis, re.DOTALL)
    
    # If the standard pattern doesn't work, try to find a list of words in the analysis
    if not criteria3_match:
        # Alternative pattern looking for word lists
        word_list_pattern = r"(?:superlative ord|overdrevne ord|ord):\s*[\"']?([\w\s,]+)[\"']?"
        criteria3_match = re.search(word_list_pattern, analysis, re.DOTALL)
    
    criteria3_result = criteria3_match.group(1).strip() if criteria3_match else "N/A"
    
    # Clean up the criteria3 result
    if criteria3_result != "N/A":
        # Remove extra whitespace and normalize formatting
        criteria3_result = re.sub(r'\s+', ' ', criteria3_result).strip()
        # Remove any leading/trailing quotes or brackets
        criteria3_result = re.sub(r'^[\[\("\']+|[\]\)"\']+$', '', criteria3_result)
    
    return {
        'criteria1': criteria1_match.group(1) if criteria1_match else "N/A",
        'criteria2': criteria2_match.group(1) if criteria2_match else "N/A",
        'criteria3': criteria3_result
    }

def process_csv(file_path):
    results = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:
                job_listing = row[0]
                prompt = construct_prompt(job_listing)
                analysis = query_openai(prompt)
                
                scores = extract_scores(analysis)
                
                results.append({
                    'job_listing': job_listing,
                    'analysis': analysis,
                    'criteria1_score': scores['criteria1'],
                    'criteria2_score': scores['criteria2'],
                    'criteria3_description': scores['criteria3']
                })
                
                # Rate limiting to avoid hitting API limits
                time.sleep(1)
    
    return results

def run_analysis():
    file_path = "/content/simplified_dataset.csv" #Endre når det settes i produksjon
    results = process_csv(file_path)
    
    # Write results to a new CSV file
    output_file = 'job_listing_analysis_results.csv'
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['job_listing', 'analysis', 'criteria1_score', 'criteria2_score', 'criteria3_description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Analysis complete. Results have been saved to {output_file}")

if __name__ == "__main__":
    run_analysis()

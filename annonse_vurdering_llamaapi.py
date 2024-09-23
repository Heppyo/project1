!pip install llamaapi

import json
from llamaapi import LlamaAPI

# Initialize the LlamaAPI with your API token
api_token = "<insert api key>"
llama = LlamaAPI(api_token)

def query_llama(prompt):
    api_request_json = {
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "max_tokens": 500  # Increase this value to allow for longer responses
    }
    
    try:
        response = llama.run(api_request_json)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def analyze_job_listing(listing):
    prompt = construct_prompt(listing)
    analysis = query_llama(prompt)
    if analysis is None:
        return "Failed to analyze job listing due to an API error."
    return analysis

def construct_prompt(job_listing):
    prompt = f"""Analyser følgende jobbannonse for bruk av "blomsterspråk", altså språk som inneholder overdreven positivitet angående stillingen. 
    Bruk det 5-poengs additive systemet beskrevet nedenfor. Gi en kort, presis analyse.

Poengskala:
1. Gi ett poeng hvis annonsen inneholder mildt positivt språk, realistisk.
2. Gi ett nytt poeng hvis annonsen inneholder språk vagt/generisk språk for å beskrive stillingen
3. Gi ett nytt poeng hvis annonsen inneholder overdrevne påstander om ansvar/kultur/fordeler.
4. Gi ett nytt poeng dersom annonsen inneholder sterk vekt på prestisje, idealisering av jobben/selskapet.
5. Gi ett siste poeng hvis annonsen inneholder språk som er overdrevent smigrende/utbrodert i nesten alle aspekter.

Jobbannonse: {job_listing}

Gi en kort analyse (maks 100 ord) som forklarer poenggivningen. Inkluder spesifikke eksempler fra teksten.

VIKTIG: 
- Svar på norsk.
- Vær konsis.
- Avslutt alltid med: "Blomstrende språk poengsum: X av 5"
"""
    return prompt

def test_prompt(job_listing):
    analysis = analyze_job_listing(job_listing)
    print("Llama API Response:")
    print(analysis)
    print("\n---\n")
    
    feedback = input("How well did the AI respond? Any tweaks needed? (Enter feedback or press Enter to skip): ")
    return feedback

def run_tests():
    while True:
        job_listing = input("Enter a job listing to analyze (or type 'quit' to exit): ")
        if job_listing.lower() == 'quit':
            break
        
        feedback = test_prompt(job_listing)
        
        if feedback:
            print("Feedback recorded:", feedback)
        
    print("Testing complete.")

# Run the tests
run_tests()

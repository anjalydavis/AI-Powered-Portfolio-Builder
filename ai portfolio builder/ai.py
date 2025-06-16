
import requests



data = {
    'name': '',
    'title': '',
    'profile_picture': '',
    'program_name_1': '',
    'program_1_university': '',
    'program1_year': '',
    'program1_skills': '',
    'program_name_2': '',
    'program_2_university': '',
    'program2_year': '',
    'program2_skills': '',
    'project1_name': '',
    'project1_description': '',
    'project1_skills': '',
    'project2_name': '',
    'project2_description': '',
    'project2_skills': '',
    'project3_name': '',
    'project3_description': '',
    'project3_skills': '',
    'email': '',
    'location': '',
    'phone': '',
    'about_me': ''
}




def call_google_ai_model(data):
    GEMINI_FLASH_API_KEY = "**************"
    GOOGLE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_FLASH_API_KEY}"

    headers= {
        'Content-Type': 'application/json'
    }


    prompt = f"""
                    Generate a professional and concise 'About Me ' section based on the user data and consider this as my about me  and generate accordingly

Name:{data['name']}
Email: {data['email']}
Phone : {data['phone']}
Title: {data['title']}
location:{data['location']}

Studies:
    -{data['program_name_1']} at {data['program_1_university']} from {data['program1_year']}  and skills i learned {data['program1_skills']}
    -{data['program_name_2']} at {data['program_2_university']} from {data['program2_year']}  and skills i learned {data['program2_skills']}



Projects:
    - name {data['project1_name']}  this is a {data['project1_description']} technologies uses {data['project1_skills']}
    - name {data['project2_name']}  this is a {data['project2_description']} technologies uses {data['project2_skills']}
    - name {data['project3_name']}  this is a {data['project3_description']} technologies uses {data['project3_skills']}



"""

    data = {
        "contents": [
        {
            "parts": [
            {
                "text": prompt.strip()
            }
            ]
        }
        ]
    }


    response = requests.post(url=GOOGLE_URL, headers=headers, json=data)
    result = response.json()['candidates'][0]['content']['parts'][0]['text']
    return result


if __name__ == "__main__":
    call_google_ai_model()
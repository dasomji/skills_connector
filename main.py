"""This code takes a list of skills, takes ten of them at a time 
(handing over more leads to bad results from GPT3.5) and hands them over to the openAI API.
The API returns a list of dictionaries where each dictionary contains: 
one skill, its type, subskill and areas that this skill is connected to.
The skills are then saved to a json-file.
For debugging: 
- the raw-data (including number of tokens used) from the API-call get saved to a log-file
- the raw-message of the API call gets saved to a text-file.
- the list of skills used for the current API call, the number of tokens used and the message-output 
"""
import json
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def get_skill_counter():
    """If no skills_counter is present, the function udpate_counter() will create a new file later."""
    try:
        with open("counter.json", "r") as counter_file:
            skills_counter = json.load(counter_file)
        return skills_counter
    except FileNotFoundError:
        skills_counter = 0
        return skills_counter


def get_number_of_skills():
    with open("skills_list.txt", "r") as skills_list:
        all_skills = skills_list.readlines()
        number_of_skills = len(all_skills)
    return number_of_skills


def get_skills_from_list(skills_counter):
    with open("skills_list.txt", "r") as skills_list:
        all_skills = skills_list.readlines()

    skills_string = ""

    for i in range(skills_counter, skills_counter+10):
        skills_string += f"{all_skills[i]}"

    return skills_string


def call_ai(skills_input):

    with open("skill_prompt_v2.txt", "r") as prompt_file:
        prompt = prompt_file.read()

    ai_response_object = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": skills_input}
        ]
    )

    # ai_response_object = client.chat.completions.create(model="gpt-3.5-turbo",
    #                                                     messages=[
    #                                                         {
    #                                                             "role": "system",
    #                                                             "content": prompt
    #                                                         },
    #                                                         {
    #                                                             "role": "user",
    #                                                             "content": skills_input
    #                                                         }
    #                                                     ],
    #                                                     temperature=1,
    #                                                     max_tokens=1000,
    #                                                     top_p=1,
    #                                                     frequency_penalty=0,
    #                                                     presence_penalty=0)

    return ai_response_object


def log_it(response_from_ai):
    """Saving both the entire OpenAI API-response as well as the content in different txt-files.
    Encountered problems with json in the beginning, therefor the redundancy."""
    content_from_ai = response_from_ai.choices[0].message.content
    with open("ai_log.txt", "a") as ai_log_file:
        ai_log_file.write(str(response_from_ai))

    with open("results.txt", "a") as ai_log_file:
        ai_log_file.write(str(content_from_ai))

    return content_from_ai


def save_generated_skills_to_json(response_from_ai):
    # fix: content_from_ai in log_it is same as content --> merge
    content = response_from_ai.choices[0].message.content
    json_content = json.loads(content)

    try:
        with open("data.json", 'r') as data_storage_file:
            data = json.load(data_storage_file)
    except FileNotFoundError:
        data = []

    for skill in json_content:
        data.append(skill)

    with open("data.json", 'w') as data_storage_file:
        json.dump(data, data_storage_file)

    return json_content


def update_counter(skills_counter):
    skills_counter += 10

    with open("counter.json", "w") as counter_file:
        json.dump(skills_counter, counter_file)

    return skills_counter


number_of_skills = get_number_of_skills()

skills_counter = get_skill_counter()

if __name__ == "__main__":
    while skills_counter <= number_of_skills:
        ten_skills = get_skills_from_list(skills_counter)
        print(ten_skills)
        print(f"OpenAI-key: {os.getenv('OPENAI_API_KEY')}")
        ai_response = call_ai(ten_skills)
        print(ai_response)
        ai_content = log_it(ai_response)
        print("----------------")
        print(ai_content)
        formatted_skills_output = save_generated_skills_to_json(ai_response)
        skills_counter = update_counter(skills_counter)
        print("------End of call----------")

Skills-connector is a tool that takes a list of skills and uses genereative AI to create subskills as well as groups to which the skill belongs to.
This is meant as a proof of concept to see wether a skill-map can be generated.
I am aware that the connections between the skills are entirely made up by the AI and aren't accurate.

E.g.: Clean Code --> Programming

Ten skills at a time are processed for quality-reasons (larger number "confuses the AI").
counter.json is used to keep track of the processed skills, so in case something breaks, one doesn't have to start all over again.

The AI is prompted to structure the response like a json-file, so that it can be saved as such.
This json-file can than be used in other tools to visualise how skills connect.

The OpenAI-API key is retrieved from a .env-file.
Instructions:

1. Create .env in the skills_connector-folder
2. Add the following:
   OPENAI_API_KEY = {your-OpenAI-API-Key}

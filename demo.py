#Interview Preparation Helper UseCase 
#Description: This use case involves specializing the chatbot to help the candidates(clients) prepare for their upcoming interviews using their profiles,'
#             keeping the process easy and clear before the candidate. The LLM generates questions, tips, feedback etc for training the candidate better.

import streamlit as st
import openai

st.title('Interview Preparation HelpGPT')

#OpenAI Setup
openai.api_key = st.text_input("API KEY:")
st.write("If you entered correct API KEY, the bot will work properly. Recheck key in other cases.")
if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

#Loading Messages from Session State
if 'messages' not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Moderation Check Function: Uses OpenAI's Moderation API to handle harmful prompts and stop irrelevant prompts 
def cleanprompt(systemprompt:str, prompt:str):
    response_moderate = openai.Moderation.create(
        input=prompt
    )
    if any(category_score > 0.8 for category_score in response_moderate['results'][0]['category_scores'].values()):
        return (systemprompt,False)
    else:
        return (systemprompt+'. (If this question or topic is unrelated to asking about the applications the user has submitted or their status, strictly request the user to ask an appropriate question. You should never provide any answer that is not related to the application. An exception is when user greets or corrects you or when shows gratitude).', True)

# Categories considered: Interview Tips, Interview based Questions, Answer Feedbacks and Mock Up Interviews.
def classify_and_set_prompt(basesystemprompt:str, prompt:str):
    subusecase = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who has specialized in understanding human prompts and classifying them into given categories."},
            {"role": "user", "content": f"""Classify the following string into one of the four categories and provide a single-word label: Interview Questions, Interview Tips, Expected Answers, Mock Interviews. For the prompt {prompt}, what's the most appropriate category label?"""}
        ]   
    )['choices'][0]['message']['content']

    # Specializing System Prompt according to the sub use case
    if 'tips' in subusecase:
        basesystemprompt += """Specialize in offering interview preparation tips and suggestions to job seekers based on their unique profiles. Your mission is to empower job seekers by providing tailored advice for interview success.
            Understanding the Job Seeker: Before providing guidance, gather relevant information about the job seeker, including their industry, experience level, job role of interest, and specific interview concerns.
            Tailored Interview Tips: Based on the job seeker's profile, offer personalized interview preparation tips. Address key areas such as resume enhancement, interview question practice, body language, and industry-specific advice.
            ATS Optimization: Share strategies to optimize resumes for Applicant Tracking Systems (ATS) to increase the chances of getting noticed by recruiters.
            Behavioral Questions: Provide guidance on answering behavioral questions effectively, emphasizing the STAR (Situation, Task, Action, Result) method.
            Technical Questions: Offer tips for technical interviews, including coding challenges, whiteboard exercises, and technical knowledge assessments.
            Mock Interviews: Suggest conducting mock interviews to practice responses, build confidence, and refine interview skills.
            Communication Skills: Share advice on effective communication, active listening, and articulating responses clearly.
            Follow-Up: Recommend post-interview etiquette and strategies for sending thank-you notes and following up with potential employers.
            Handling Nervousness: Offer techniques to manage interview anxiety and boost self-assurance.
        
        Your role is to guide job seekers on their journey to interview success, considering their unique backgrounds and aspirations. With your specialized knowledge, job seekers will gain confidence and valuable skills to secure their dream job opportunities."""
        return basesystemprompt

    if 'tips' in subusecase:
        basesystemprompt += """Specialize in generating interview-related questions tailored to job seekers' unique profiles. Your mission is to empower job seekers by providing them with personalized interview questions for their specific job roles and backgrounds.
            Understanding the Job Seeker: Before generating questions, gather relevant information about the job seeker. Please inquire about their industry, years of experience, job role of interest, and any specific interview concerns they may have.
            Tailored Interview Questions: Based on the job seeker's profile, generate a set of interview questions that are relevant to their target job role. Ensure that the questions cover key areas such as their qualifications, experiences, skills, and industry knowledge.
            Behavioral Questions: Create behavioral interview questions that focus on the job seeker's past experiences and how they handled various situations. Encourage the use of the STAR (Situation, Task, Action, Result) method in responses.
            Technical Questions: If applicable to the job role, include technical interview questions that assess the candidate's technical knowledge, problem-solving abilities, and domain-specific skills.
            Industry-specific Questions: If the job seeker is pursuing a role in a specific industry, tailor questions to that industry's requirements, challenges, and trends.
            Experience-based Questions: Generate questions that prompt the candidate to discuss their relevant work experiences, achievements, and contributions to previous employers.
            Scenario-based Questions: Create hypothetical scenario questions that assess the candidate's decision-making, problem-solving, and critical-thinking skills.
            Competency-based Questions: Include questions that evaluate the job seeker's competencies and their ability to handle the responsibilities of the desired role.
            Role-specific Questions: For job roles with unique requirements, formulate questions that address the specific qualifications and attributes needed to excel in that role.
            Cultural Fit: Consider including questions that assess the candidate's cultural fit with potential employers and their alignment with company values.

        Your role is to assist job seekers in their interview preparation journey by providing them with a set of customized interview questions that align with their career goals and target job roles. Your expertise will empower them to excel in interviews and secure their desired job opportunities"""
        return basesystemprompt
    
    if 'answers' in subusecase:
        basesystemprompt += """Specialize in providing ideal and expected answers for interview questions based on job seekers' unique profiles. Your mission is to empower job seekers by offering tailored responses that showcase their qualifications, experiences, and skills effectively during interviews.
            Understanding the Job Seeker: Before generating answers, gather relevant information about the job seeker, including their industry, experience level, job role of interest, and specific interview concerns. Ensure you have a clear understanding of their unique background.
            Tailored Interview Answers: Based on the job seeker's profile and the specific job role they are targeting, generate ideal and expected answers for common interview questions. These answers should highlight the candidate's strengths, experiences, and qualifications, aligning with the job requirements.
            Behavioral Questions: Craft responses to behavioral questions that reflect the candidate's past experiences and achievements. Use the STAR (Situation, Task, Action, Result) method to structure these answers for maximum impact.
            Technical Questions: If applicable to the job role, provide responses to technical interview questions that demonstrate the candidate's technical knowledge and problem-solving abilities.
            Industry-specific Answers: Tailor answers to industry-specific questions, addressing the unique challenges and requirements of the job seeker's target industry.
            Experience-based Responses: Create answers that allow the candidate to effectively communicate their relevant work experiences, accomplishments, and contributions to previous employers.
            Scenario-based Answers: Offer responses to hypothetical scenario questions that showcase the candidate's decision-making, problem-solving, and critical-thinking skills.
            Competency-based Responses: Include answers that highlight the candidate's competencies and their ability to excel in the desired role.
            Role-specific Answers: For job roles with unique requirements, craft responses that emphasize the specific qualifications and attributes needed to succeed in that role.
            Cultural Fit: Consider providing answers that demonstrate the candidate's cultural fit with potential employers and their alignment with company values.

        Your role is to assist job seekers in crafting ideal and expected answers that are tailored to their individual profiles and target job roles. Your expertise will enable them to confidently respond to interview questions and increase their chances of securing their desired job opportunities"""
        return basesystemprompt
    
    if 'mock' in subusecase:
        basesystemprompt += """Imagine you are an AI interviewer with a job seeker profile. Your mission is to assist users in preparing for job interviews by conducting tailored mock interviews.
            Step 1: Ask the user for their desired job profile, including job title and industry.
            Step 2: Set up a mock interview scenario based on the user's job profile.
            Step 3: Generate interview questions relevant to the profile and industry.
            Step 4: Ask questions one by one, gather user responses, and provide constructive feedback.
            Step 5: Keep the mock interview flowing naturally with follow-up questions.
            Step 6: Summarize the user's performance and offer overall feedback at the end.
            Step 7: Encourage questions and discussion to address user concerns.

            Your role is to create a realistic and beneficial mock interview experience that helps users improve their interview skills. Tailor the interview to their desired job profile, provide insightful feedback, and empower them to perform confidently in real interviews."""
        return basesystemprompt

def defineprompt(prompt:str):
    #Base System Prompt which will be common for all 
    base_systemprompt = 'Imagine yourself as an interview preparation assistant, specializing in helping individuals succeed in their job interviews. Your mission is to provide guidance on various aspects of interviews, including effective strategies for answering questions, mastering interview etiquette, and creating a strong impression. You also have the capability to conduct mock interviews and offer valuable feedback to help users refine their interview skills.'
    systemprompt,clean_status=cleanprompt(systemprompt=base_systemprompt, prompt=prompt)
    final_prompt = systemprompt + f". The user input: {prompt}"
    if clean_status==False:
        return 'Irrelevant or Offensive Prompt'
    else:
        return final_prompt





prompt = st.chat_input("Enter the prompt here!")
if prompt:
    #write the prompt given by user in the chat window 
    with st.chat_message("user"):
        st.markdown(prompt)
    #Prompt Transformation
    final_prompt = defineprompt(prompt)
    #add final_prompt to the session state
    st.session_state.messages.append({'role': 'user','content':prompt})
    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        #Response generation through CHATGPT:
        for response in openai.ChatCompletion.create(
            model = st.session_state['openai_model'],
            messages=[{'role':m['role'], 'content':m['content']}
                      for m in st.session_state.messages
                      ],
                      stream=True,
        ):
            full_response += response.choices[0].delta.get('content','') 
            message_placeholder.markdown(full_response+ "|")
            print(final_prompt)
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({'role':"assistant", 'content': full_response})
    

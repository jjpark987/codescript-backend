from dotenv import load_dotenv
from ollama import Client
from os import getenv, path
from re import search, DOTALL

load_dotenv()

def create_prompt(problem: dict, submission: str) -> str:
    prompt = f'''
        ### System Instructions:
        You do not remember any past conversations. Treat this as a completely new session with no prior knowledge.

        ### Scenario:
        You are my professor specializing in coding problems. I will describe my submission for solving a problem, and you will analyze and provide structured feedback on my submission to a valid solution. Respond to me like a human, using "you" instead of "the user."

        ### My Submission (FOCUS ON THIS AND PROVIDE FEEDBACK): 
        {submission}

        ### Instructions:
        - **STOP**. Read and evaluate my submission before doing anything else. Your only purpose is to analyze my submission.
        - If my submission does not attempt to solve the problem, is unrelated to solving the problem, or tells you "I don't know", explicitly state that in the analysis, provide two starting suggestions, score it as 1, and **skip Problem Details.**
        - DO NOT generate explanations, reasoning, or additional insights beyond what is explicitly written in my submission.

        ### Expected Output (FOLLOW THIS EXACTLY):
        Analysis: 
            <Provide feedback on my submission in full sentences if related; otherwise, explicitly state that my submission is unrelated> 
        Suggestions: 
            - <Bullet point suggestions if related; otherwise, provide two general starting points>
        Score: 
            <
                Integer 1, 2, or 3:
                3 → The submission is valid within given constraints.
                2 → The submission is technically valid but inefficient for larger constraints or needs improvements.
                1 → The submission is fundamentally incorrect or is unrelated to solving coding problems.
            >
        
        ### Problem Details (FOR REFERENCE ONLY, IGNORE THIS IF MY SUBMISSION IS UNRELATED):
        Title: {problem['title']}
        Description: {problem['description']}
        Constraints: {''.join([f'{constraint}' for constraint in problem['constraints']])}
        Examples: {chr(10).join([f'Input: {example['input']}, Output: {example['output']}, Explanation: {example['explanation']}' for example in problem['examples']])}
    '''
    
    return prompt

def ask_model(prompt: str):
    try:
        response = Client(host=getenv('OLLAMA_HOST_URL')).generate(model='deepseek-r1:7b', prompt=prompt)
        return response['response']
    except Exception as e:
        print(f'❌ Error sending request to ollama client: {e}')

def parse_response(response: str) -> dict:
    if not response:
        print('❌ Model did not give a response')
        return {
            'analysis': '',
            'suggestions': [],
            'score': 0
        }

    analysis_match = search(r'Analysis:\s*(.*?)(?=\nSuggestions:)', response, DOTALL)
    suggestions_match = search(r'Suggestions:\s*(.*?)(?=\nScore:)', response, DOTALL)
    score_match = search(r'Score:\s*(\d+)', response)

    analysis = analysis_match.group(1).strip() if analysis_match else ''
    suggestions = [s.strip('- ') for s in suggestions_match.group(1).strip().split("\n")] if suggestions_match else []
    score = int(score_match.group(1)) if score_match else 0

    return {
        'analysis': analysis,
        'suggestions': suggestions,
        'score': score
    }

def run_deepseek(problem: dict, submission: str):
    prompt = create_prompt(problem, submission)
    response = ask_model(prompt)
    return parse_response(response)

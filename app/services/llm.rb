require 'dotenv/load'
require 'faraday'
require 'json'

class LlmService
  MODEL = ENV['MODEL']
  OLLAMA_HOST_URL = ENV['OLLAMA_HOST_URL']

  def self.run(problem, submission)
    prompt = create_prompt(problem, submission)
    response = ask_model(prompt)
    Rails.logger.info("📥 Raw LLM response: #{response.inspect}")
    parse_response(response)
  end

  def self.create_prompt(problem, submission)
    examples = problem['examples'].map do |example|
      "Input: #{example['input']}, Output: #{example['output']}, Explanation: #{example['explanation']}"
    end.join("\n")

    constraints = problem['constraints'].join

    <<~PROMPT
      ### System Instructions:
      You do not remember any past conversations. Treat this as a completely new session with no prior knowledge.

      ### Scenario:
      You are my professor specializing in coding problems. I will present my submission for solving a problem and you will analyze and provide structured feedback on my submission to any valid solution to the problem. YOU ARE SCORING MY SUBMISSION BASED ON THE SOUNDNESS OF MY LOGIC. YOU DO NOT NEED ME TO SUBMIT CODE IMPLEMENTATION TO SCORE ME.

      ### My Submission (FOCUS ON THIS AND PROVIDE FEEDBACK):
      #{submission}

      ### Instructions:
      - **STOP**. Read and evaluate my submission before doing anything else. Your only purpose is to analyze my submission.
      - My submission will be any one of these:
          1. A blank submission, an unrelated submission or I tell you "I don't know" or "I need help".
          2. My approach to the solution in words using just words explaining the steps WITHOUT code implementation.
          3. The actual code implementation.
      - First categorize my submission into one of the three categories above.
      - If my submission is category 1: 
          - Provide at least two starting suggestions that are specific to the problem and will help me toward a solution.
          - Score it as 1.
          - Skip Problem Details below.
      - If my submission is category 2 or 3:
          - If my logic is correct and valid under the constraints (EVEN IF IT MAY NOT BE OPTIMIZED AND THERE IS NO ACTUAL CODE IMPLEMENTATION):
              - State clearly that you have no further suggestions for me or provide some helpful optional tips pertaining to my submission.
              - Score it as 3.
          - If my logic is correct but inefficient for the constraints or needs a few improvements in the logic:
              - Provide suggestions that are specific to the problem and will help me to complete my submission. If I submitted category 1, these suggestions should help me find the correct logic in words. If I submitted category 2 or 3, these suggestions should help me create the correct code solution.
              - Score it as 2.
          - If my logic is fundamentally flawed for this problem and constraints:
              - Provide at least two starting suggestions that are specific to the problem and will help me toward a solution.
              - Score it as 1.
      - Refer to me as "you", the submission as "your submission", and approach as "your approach".

      ### DO NOT MENTION THESE IN ANY PARTS OF YOUR RESPONSE (IMPORTANT):
          - The four categories shown above. These categories are only for your reference.
          - Setting up import statements. The focus of your analysis is on the logic of my submission not import statements.
          - What kind of language I will be using. The focus of your analysis is on the logic of my submission not what kind of language I will be using.
          - Including code implementation as an improvement. You are fully capable of scoring me without seeing a code implementation since you are focused on my logic.
      
      ### YOUR OUTPUT (FOLLOW THIS FORMAT EXACTLY WORD FOR WORD NO MATTER WHAT):
      Analysis: 
          <Provide feedback on my submission in full sentences.>
      Suggestions: 
          - <Bullet point suggestions.>
      Score: 
          <ONLY one integer: 1, 2, or 3. Do NOT provide any explanation here.>
      
      ### Problem Details (FOR REFERENCE ONLY, IGNORE THIS IF MY SUBMISSION IS UNRELATED OR BLANK):
      Title: #{problem['title']}
      Description: #{problem['description']}
      Constraints: #{problem['constraints'].join(', ')}
      Examples: #{problem['examples'].map { |example| "Input: #{example['input']}, Output: #{example['output']}, Explanation: #{example['explanation']}" }.join("\n")}"
    PROMPT
  end

  def self.ask_model(prompt)
    conn = Faraday.new(url: ENV['OLLAMA_HOST_URL']) do |f|
      f.request :json
      f.response :json
      f.adapter Faraday.default_adapter
    end
  
    res = conn.post('/api/generate', { model: ENV['MODEL'], prompt: prompt, stream: false })
  
    res.body['response']
  end

  def self.parse_response(response)
    return { analysis: '', suggestions: [], score: 0 } if response.nil?

    analysis = response[/Analysis:\s*(.*?)(?=\nSuggestions:)/m, 1]&.strip || ''
    suggestions_text = response[/Suggestions:\s*(.*?)(?=\nScore:)/m, 1]&.strip || ''
    suggestions = suggestions_text.lines.map { |line| line.gsub(/^[-•]\s*/, '').strip }
    score = response[/Score:\s*(\d+)/, 1].to_i

    {
      analysis: analysis,
      suggestions: suggestions,
      score: score
    }
  end
end

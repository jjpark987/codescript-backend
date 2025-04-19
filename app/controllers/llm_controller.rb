class LlmController < ApplicationController
  def generate_feedback
    problem_data = params[:problem_data] || params.dig(:llm, :problem_data)
    submission = params[:user_submission] || params.dig(:llm, :user_submission)

    feedback = LlmService.run(problem_data, submission)
    render json: feedback
  end
end

class LlmController < ApplicationController
  def generate_feedback
    problem_data = params[:problem_data]
    submission = params[:user_submission]

    feedback = LlmService.run(problem_data, submission)
    render json: feedback
  end
end

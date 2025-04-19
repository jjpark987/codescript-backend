class ProblemsController < ApplicationController
  def create
    problem = Problem.new(problem_params)
    if problem.save
      render json: problem, status: :created
    else
      render json: { errors: problem.errors.full_messages }, status: :unprocessable_entity
    end
  end

  def random
    problem = Problem.order('RANDOM()').first
    render json: {
      problem: ProblemSerializer.new(problem),
      image_urls: problem.image_paths
    }
  end

  private

  def problem_params
    params.require(:problem).permit(:subcategory_id, :title, :difficulty, :description, constraints: [], examples: [:input, :output, :explanation], image_paths: [])
  end
end

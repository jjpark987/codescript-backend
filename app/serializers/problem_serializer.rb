class ProblemSerializer < ActiveModel::Serializer
  attributes :title, :difficulty, :description, :constraints, :examples
end

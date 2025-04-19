class Problem < ApplicationRecord
  belongs_to :subcategory

  validates :title, presence: true, length: { maximum: 255 }
  validates :difficulty, inclusion: { in: [1, 2, 3] }
  validates :description, presence: true
  validates :constraints, :examples, presence: true

  def to_s
    title
  end
end

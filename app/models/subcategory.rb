class Subcategory < ApplicationRecord
  belongs_to :category
  has_many :problems, dependent: :destroy

  validates :name, presence: true, uniqueness: true, length: { maximum: 100 }
  validates :description, length: { maximum: 255 }, allow_blank: true

  def to_s
    name
  end
end

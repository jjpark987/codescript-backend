class CreateProblems < ActiveRecord::Migration[8.0]
  def change
    create_table :problems do |t|
      t.string :title
      t.integer :difficulty
      t.text :description
      t.json :constraints
      t.json :examples
      t.json :image_paths
      t.references :subcategory, null: false, foreign_key: true

      t.timestamps
    end
  end
end

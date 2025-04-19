# This file should ensure the existence of records required to run the application in every environment (production,
# development, test). The code here should be idempotent so that it can be executed at any point in every environment.
# The data can then be loaded with the bin/rails db:seed command (or created alongside the database with db:setup).
#
# Example:
#
#   ['Action', 'Comedy', 'Drama', 'Horror'].each do |genre_name|
#     MovieGenre.find_or_create_by!(name: genre_name)
#   end

puts 'Seeding categories...'

categories_to_add = [
  { name: 'data manipulations', description: 'Focuses on transforming, rearranging, or deriving results from data.' },
  { name: 'combinatorics', description: 'Explores counting or generating combinations, permutations, and subsets.' },
  { name: 'optimizations', description: 'Aims to find optimal solutions by maximizing or minimizing specific criteria.' }
]

categories_to_add.each do |category_data|
  Category.find_or_create_by(name: category_data[:name]) do |category|
    category.description = category_data[:description]
  end
end

puts 'Seeding subcategories...'

subcategories_to_add = [
  { name: 'reformatting', description: 'Focuses on rearranging and transforming data.', category_name: 'data manipulations' },
  { name: 'reducing', description: 'Involves summarizing or aggregating data.', category_name: 'data manipulations' },
  { name: 'counting', description: 'Deals with counting elements or sets.', category_name: 'combinatorics' },
  { name: 'generating', description: 'Focuses on creating combinations, permutations, or subsets.', category_name: 'combinatorics' },
  { name: 'strings', description: 'Optimization problems focused on string manipulation.', category_name: 'optimizations' },
  { name: 'arrays', description: 'Optimizing solutions for array-based problems.', category_name: 'optimizations' },
  { name: 'structures', description: 'Optimization for graphs, trees, grids, or matrices.', category_name: 'optimizations' },
  { name: 'heaps', description: 'Focuses on heap-based data structures.', category_name: 'optimizations' },
  { name: 'processes', description: 'Optimizes processes like scheduling or workflows.', category_name: 'optimizations' }
]

subcategories_to_add.each do |subcategory_data|
  category = Category.find_by(name: subcategory_data[:category_name])
  next unless category

  Subcategory.find_or_create_by(name: subcategory_data[:name]) do |subcategory|
    subcategory.description = subcategory_data[:description]
    subcategory.category_id = category.id
  end
end

puts '✅ Done seeding'

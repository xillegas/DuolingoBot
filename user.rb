# Modelo User para usuarios de Duolingo
class User
  attr_reader :username, :total_xp, :streak, :crowns

  def initialize(data = {})
    # Todas las key del hash data deben coincidir con el json de duolingo
    @username = data['username']
    @total_xp = data['totalXp']
    @streak = data['streak']
    @crowns = crowns_counter(data['courses'])
    @id = data['id']
  end

  def crowns_counter(all_courses)
    total_crowns = 0
    all_courses.each do |hash|
      total_crowns += hash['crowns']
    end
    total_crowns
  end
end

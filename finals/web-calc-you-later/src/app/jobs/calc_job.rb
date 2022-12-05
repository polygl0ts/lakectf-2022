require "safe_ruby"
class CalcJob < ApplicationJob
  queue_as :default

  def perform(program, user)
    res = SafeRuby.eval(program)
    Result.new(result: res.to_s, user: user).save
  end
end

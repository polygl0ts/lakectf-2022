class UserController < ApplicationController
  def index
  end
  
  def login
    user = User.find_by(username: params[:username])
    if user == nil then
      user = User.new(username: params[:username], password: params[:password])
      user.save
      puts "Create user #{user.username}"
    end
    if user.password == params[:password] then
      puts "Logged in user #{user.username}"
      session[:user] = user.username
      redirect_to controller: :home, action: :index
    else
      puts "Failed login for #{user.username}"
      render :index
    end
  end
end

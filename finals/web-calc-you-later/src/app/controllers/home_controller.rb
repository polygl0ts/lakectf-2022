class HomeController < ApplicationController
  def index
    redirect_to controller: :user, action: :index unless session[:user]
    @user = User.find_by(username: session[:user])
    @results = Result.where(user: @user).order(created_at: :desc).limit(10)
  end
  
  def post 
    redirect_to controller: :user, action: :index unless session[:user]
    @user = User.find_by(username: session[:user])
    CalcJob.set(wait: 1.minutes).perform_later(params[:program], @user)
    redirect_to action: :index
  end
end

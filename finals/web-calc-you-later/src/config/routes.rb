Rails.application.routes.draw do
  get 'user/login', to: "user#index"
  post 'user/login', to: "user#login"
  root 'home#index'
  post '/', to: "home#post"
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
end

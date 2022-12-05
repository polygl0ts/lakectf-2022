FROM ruby:3.1.2

COPY src/ /app
COPY master.key /app/config/master.key
COPY flag secret getflag /
RUN chmod 4511 /getflag && chmod 400 /flag /secret
WORKDIR /app
ENV RAILS_ENV=production
RUN bin/bundle
RUN bin/rails db:prepare && bin/rake assets:precompile
RUN chmod -R 755 /app && chown -R root:root /app
RUN useradd rails && chown -R rails /app/tmp && chmod -R o+w /app/log && chown rails /app/db /app/db/production.sqlite3
USER rails

CMD ["bin/rails", "server", "-b", "0", "-e", "production"]

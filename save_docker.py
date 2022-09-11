version: '3.3'
services:
  # web_scraper:
  #   image: 8eb23ce5b731
  #   restart: always
  #   ports:
  #     - 8080:8080

  database:
    image: postgres
    ports:
      - '5438:5432'
    restart: always
    # depends_on:
    #   - web_scraper
    environment:
      - POSTGRES_USER=docker
      - POSTGRES_PASSWORD=dance
      - POSTGRES_DB=postgres

  

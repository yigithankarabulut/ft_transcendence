# FT_Trasncendence

Ecole 42 Commen Core müfredatının son projesi. Klasik Pong oyununun gelişmiş bir versiyonunu, AI rakipleri, uzaktan çok oyunculu yetenekler ve sağlam kullanıcı kimlik doğrulaması içeren bir mikroservis mimarisi kullanarak oluşturuldu. Frontend Single Page Application şeklinde Pure JS ile geliştirildi. Backend Django Rest Framework ile geliştirildi. 

Project Subject: https://cdn.intra.42.fr/pdf/pdf/117706/en.subject.pdf

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Architecture](#architecture)

## Introduction
This project aims to create an enhanced version of the Pong game with a focus on scalability, security, and advanced gameplay features. By leveraging microservices architecture and modern web technologies, we've built a robust platform that goes beyond the traditional Pong experience.

## Features
- **Microservices Architecture**: Backend designed as microservices for improved scalability and maintainability.
- **User Management**: Standard user management system with authentication across tournaments.
- **Remote Authentication**: Implement secure remote authentication for users.
- **Two-Factor Authentication (2FA)**: Enhanced security with 2FA and JWT (JSON Web Tokens).
- **AI Opponent**: Challenge yourself against an intelligent AI player.
- **Remote Multiplayer**: Play against other players remotely.
- **Server-Side Pong**: Core game logic implemented on the server for fair play.
- **RESTful API**: Full-featured API for game interactions and data management.
- **Frontend Framework**: Modern, responsive user interface built with a frontend framework/toolkit.
- **Database Integration**: Robust data management using a backend database.

## Installation
To set up this project, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yigithankarabulut/ft_transcendence.git
   cd ft_transcendence

2. **Edit .env file**\
  Edit .env files for both frontend and backend with necessary configurations

4. **Run with Docker Compose**
   ```sh
   docker-compose up --build
   

## Architecture
Our microservices architecture includes the following components:

1. **API Gateway**\
  Entry point for client requests, routing to appropriate services
2. **Authentication Service**\
  Provides authentication for requests to internal services. ApiGateway sends requests to the auth service as a middleware for all requests except Excluded Routes
3. **User Management Service**\
  Manages user management and authentication
4. **Friend Service**\
  Handles users' friendships.
5. **Bucket Service**\
  Service that stores and serves files such as Media, Photo, etc.
6. **Game Playing Service**\
  Service that processes the game on the server side. It has a Websocket consumer and connects to wss.
7. **Game Service**\
  Manages game logic and state
8. **Mail Service**\
  A consumer that consumes RabbitMQ. Asnyc handles cases such as 2FA code, Email verification, Forgot Password.
9. **Status Service**\
  Handles online/offline status of users.

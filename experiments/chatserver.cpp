#include "chat_server.hpp"
#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>

ChatServer::ChatServer(int port) : port(port) {}

void ChatServer::start() {
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("Socket failed"); return; }

    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_fd, (sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        return;
    }

    listen(server_fd, 10);
    std::cout << "ChatServer running on port " << port << std::endl;

    std::thread(&ChatServer::accept_connections, this).detach();

    while (true) std::this_thread::sleep_for(std::chrono::seconds(1));
}

void ChatServer::accept_connections() {
    while (true) {
        int client_socket = accept(server_fd, nullptr, nullptr);
        if (client_socket >= 0) {
            std::lock_guard<std::mutex> lock(client_mutex);
            clients.push_back(client_socket);
            std::thread(&ChatServer::handle_client, this, client_socket).detach();
        }
    }
}

void ChatServer::handle_client(int client_socket) {
    char buffer[1024];
    while (true) {
        ssize_t bytes = recv(client_socket, buffer, 1024, 0);
        if (bytes <= 0) break;
        broadcast(std::string(buffer, bytes), client_socket);
    }
}

void ChatServer::broadcast(const std::string& msg, int sender_socket) {
    std::lock_guard<std::mutex> lock(client_mutex);
    for (int client : clients)
        if (client != sender_socket)
            send(client, msg.c_str(), msg.size(), 0);
}
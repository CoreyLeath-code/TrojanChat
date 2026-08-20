#ifndef CHAT_SERVER_HPP
#define CHAT_SERVER_HPP

#include <string>
#include <vector>
#include <thread>
#include <mutex>
#include <netinet/in.h>

class ChatServer {
public:
    ChatServer(int port);
    void start();

private:
    int server_fd;
    int port;
    std::vector<int> clients;
    std::mutex client_mutex;

    void accept_connections();
    void handle_client(int client_socket);
    void broadcast(const std::string& msg, int sender_socket);
};

#endif
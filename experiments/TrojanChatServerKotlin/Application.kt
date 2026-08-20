TrojanChatServerKotlin/src/main/kotlin/com/yourorg/trojanchat/Application.kt

package com.yourorg.trojanchat

import io.ktor.server.engine.*
import io.ktor.server.netty.*
import io.ktor.server.application.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.routing.*
import io.ktor.server.websocket.*
import io.ktor.websocket.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.time.Duration
import java.util.concurrent.*

@Serializable
data class Message(val id: String, val sender: String, val content: String, val timestamp: String)

fun main() {
    // Thread-safe set of connected sessions
    val connections = ConcurrentLinkedQueue<DefaultWebSocketServerSession>()

    embeddedServer(Netty, port = 8080) {
        install(ContentNegotiation) {
            json(Json { prettyPrint = true })
        }
        install(WebSockets) {
            pingPeriod = Duration.ofSeconds(15)
            timeout = Duration.ofSeconds(30)
            maxFrameSize = Long.MAX_VALUE
            masking = false
        }
        routing {
            webSocket("/chat") {
                // New client connected
                connections.add(this)
                try {
                    // Listen for incoming frames
                    for (frame in incoming) {
                        frame as? Frame.Text ?: continue
                        val text = frame.readText()
                        // Broadcast to all connections
                        connections.forEach { session ->
                            session.send(Frame.Text(text))
                        }
                    }
                } finally {
                    // Remove on disconnect
                    connections.remove(this)
                }
            }
        }
    }.start(wait = true)
}

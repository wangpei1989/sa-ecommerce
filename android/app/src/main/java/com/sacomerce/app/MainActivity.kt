package com.sacomerce.app

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException

class MainActivity : AppCompatActivity() {

    private lateinit var messagesRecyclerView: RecyclerView
    private lateinit var messageAdapter: MessageAdapter
    private lateinit var messageInput: EditText
    private lateinit var sendButton: ImageButton

    // TODO: Replace with your deployed Agent API URL and Token
    private var apiBaseUrl = "https://your-agent-api.coze.cn"
    private var apiToken = "your_api_token_here"

    private val client = OkHttpClient()
    private val gson = Gson()

    private val messages = mutableListOf<Message>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        initViews()
        setupRecyclerView()
        setupListeners()

        // Add welcome message
        addMessage("assistant", "👋 Welcome to SA Commerce!\n\nI'm your shopping assistant. How can I help you today?\n\nTry:\n• Search for products\n• Check your cart\n• Track orders\n• Currency conversion")
    }

    private fun initViews() {
        messagesRecyclerView = findViewById(R.id.messagesRecyclerView)
        messageInput = findViewById(R.id.messageInput)
        sendButton = findViewById(R.id.sendButton)
    }

    private fun setupRecyclerView() {
        messageAdapter = MessageAdapter(messages)
        messagesRecyclerView.layoutManager = LinearLayoutManager(this)
        messagesRecyclerView.adapter = messageAdapter
    }

    private fun setupListeners() {
        sendButton.setOnClickListener {
            val message = messageInput.text.toString().trim()
            if (message.isNotEmpty()) {
                sendMessage(message)
            }
        }
    }

    private fun sendMessage(message: String) {
        // Add user message
        addMessage("user", message)
        messageInput.text.clear()

        // Send to Agent API
        sendToAgent(message)
    }

    private fun sendToAgent(message: String) {
        val json = """
            {
                "message": "$message"
            }
        """.trimIndent()

        val requestBody = json.toRequestBody("application/json".toMediaType())

        val request = Request.Builder()
            .url(apiBaseUrl)
            .addHeader("Authorization", "Bearer $apiToken")
            .addHeader("Content-Type", "application/json")
            .post(requestBody)
            .build()

        // Show loading
        addMessage("assistant", "💭 Thinking...")

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    // Remove loading message
                    messages.removeAt(messages.size - 1)
                    addMessage("assistant", "❌ Error: ${e.message}\n\nPlease check your API configuration.")
                }
            }

            override fun onResponse(call: Call, response: Response) {
                runOnUiThread {
                    // Remove loading message
                    if (messages.size > 0 && messages[messages.size - 1].content == "💭 Thinking...") {
                        messages.removeAt(messages.size - 1)
                    }
                    
                    val responseBody = response.body?.string() ?: "No response"
                    addMessage("assistant", responseBody)
                }
            }
        })
    }

    private fun addMessage(role: String, content: String) {
        messages.add(Message(role, content))
        messageAdapter.notifyItemInserted(messages.size - 1)
        messagesRecyclerView.scrollToPosition(messages.size - 1)
    }
}

data class Message(val role: String, val content: String)

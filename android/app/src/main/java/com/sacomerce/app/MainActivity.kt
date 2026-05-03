package com.sacomerce.app

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity() {
    
    private lateinit var messageInput: EditText
    private lateinit var sendButton: Button
    private lateinit var chatView: TextView
    private lateinit var scrollView: ScrollView
    
    private val client = OkHttpClient.Builder()
        .connectTimeout(60, TimeUnit.SECONDS)
        .readTimeout(120, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
        .build()
    
    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())
    
    // Replace with your deployed API endpoint
    private var apiBaseUrl = "https://your-agent-api.coze.cn"
    private var apiToken = "your_api_token_here"
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        loadConfig()
        appendMessage("🤖 SA Commerce Bot", "Welcome to South Africa E-Commerce!\n\nHow can I help you today?")
    }
    
    private fun initViews() {
        messageInput = findViewById(R.id.messageInput)
        sendButton = findViewById(R.id.sendButton)
        chatView = findViewById(R.id.chatView)
        scrollView = findViewById(R.id.scrollView)
        
        sendButton.setOnClickListener { sendMessage() }
        messageInput.setOnEditorActionListener { _, _, _ ->
            sendMessage()
            true
        }
    }
    
    private fun loadConfig() {
        // Load API configuration from SAConfig
        val config = SAConfig(this)
        apiBaseUrl = config.getApiBaseUrl()
        apiToken = config.getApiToken()
    }
    
    private fun sendMessage() {
        val message = messageInput.text.toString().trim()
        if (message.isEmpty()) return
        
        appendMessage("You", message)
        messageInput.text.clear()
        
        scope.launch {
            try {
                val response = withContext(Dispatchers.IO) {
                    callApi(message)
                }
                appendMessage("🤖 SA Commerce Bot", response)
            } catch (e: Exception) {
                appendMessage("🤖 SA Commerce Bot", "Sorry, an error occurred: ${e.message}")
            }
        }
    }
    
    private fun callApi(message: String): String {
        val json = JSONObject().apply {
            put("query", message)
            put("stream", false)
            put("conversation_id", "mobile_user")
        }
        
        val body = json.toString().toRequestBody("application/json".toMediaType())
        
        val request = Request.Builder()
            .url("$apiBaseUrl/chat")
            .addHeader("Authorization", "Bearer $apiToken")
            .addHeader("Content-Type", "application/json")
            .post(body)
            .build()
        
        return client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                throw IOException("API Error: ${response.code}")
            }
            response.body?.string() ?: "No response"
        }
    }
    
    private fun appendMessage(sender: String, message: String) {
        runOnUiThread {
            val currentText = chatView.text.toString()
            val newText = if (currentText.isEmpty()) {
                "【$sender】\n$message\n\n"
            } else {
                "$currentText【$sender】\n$message\n\n"
            }
            chatView.text = newText
            scrollView.post { scrollView.fullScroll(View.FOCUS_DOWN) }
        }
    }
    
    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
        client.dispatcher.executorService.shutdown()
    }
}

package com.sacomerce.app

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class MessageAdapter(private val messages: List<Message>) :
    RecyclerView.Adapter<MessageAdapter.MessageViewHolder>() {

    inner class MessageViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val messageText: TextView = itemView.findViewById(R.id.messageText)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MessageViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_message, parent, false)
        return MessageViewHolder(view)
    }

    override fun onBindViewHolder(holder: MessageViewHolder, position: Int) {
        val message = messages[position]
        holder.messageText.text = message.content
        
        // Style based on role
        val params = holder.messageText.layoutParams as android.widget.FrameLayout.LayoutParams
        if (message.role == "user") {
            params.gravity = android.view.Gravity.END
            holder.itemView.setBackgroundResource(R.drawable.user_message_bg)
        } else {
            params.gravity = android.view.Gravity.START
            holder.itemView.setBackgroundResource(R.drawable.assistant_message_bg)
        }
        holder.messageText.layoutParams = params
    }

    override fun getItemCount(): Int = messages.size
}

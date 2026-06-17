package com.flowmoney.receivers

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import com.flowmoney.domain.SmsParser
import com.flowmoney.workers.SmsUploadWorker

class SmsReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Telephony.Sms.Intents.SMS_RECEIVED_ACTION) {
            val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
            for (sms in messages) {
                val messageBody = sms.messageBody
                val timestamp = sms.timestampMillis
                
                // Fast check
                val parsed = SmsParser.parse(messageBody)
                if (parsed != null) {
                    Log.d("SmsReceiver", "UPI Transaction detected: $messageBody")
                    
                    // In production, save to Room DB here before queueing worker
                    
                    // Queue background upload
                    val workData = workDataOf(
                        "raw_sms" to messageBody,
                        "received_at" to timestamp
                    )
                    
                    val uploadWork = OneTimeWorkRequestBuilder<SmsUploadWorker>()
                        .setInputData(workData)
                        .build()
                        
                    WorkManager.getInstance(context).enqueue(uploadWork)
                }
            }
        }
    }
}

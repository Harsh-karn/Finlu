package com.flowmoney.workers

import android.content.Context
import android.util.Log
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

class SmsUploadWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        val rawSms = inputData.getString("raw_sms") ?: return Result.failure()
        val receivedAtMillis = inputData.getLong("received_at", System.currentTimeMillis())
        
        // Format ISO date
        val sdf = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US)
        sdf.timeZone = TimeZone.getTimeZone("UTC")
        val isoDate = sdf.format(Date(receivedAtMillis))
        
        // Get API Key from SharedPreferences in real app
        val deviceApiKey = "mock_api_key_from_shared_prefs" 
        
        val json = JSONObject().apply {
            put("raw_sms", rawSms)
            put("received_at", isoDate)
            put("device_api_key", deviceApiKey)
        }
        
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)
        
        val request = Request.Builder()
            .url("http://10.0.2.2:8000/api/v1/sms/ingest") // Emulator to localhost
            .post(body)
            .build()
            
        val client = OkHttpClient()
        
        return try {
            val response = client.newCall(request).execute()
            if (response.isSuccessful) {
                Log.d("SmsUploadWorker", "Successfully uploaded SMS")
                Result.success()
            } else {
                Log.e("SmsUploadWorker", "Failed to upload: ${response.code}")
                Result.retry()
            }
        } catch (e: Exception) {
            Log.e("SmsUploadWorker", "Error uploading SMS", e)
            Result.retry()
        }
    }
}

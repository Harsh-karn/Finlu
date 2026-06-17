package com.example.flowmoney.domain

import java.util.regex.Pattern

data class ParsedSms(
    val amount: Long,
    val type: String, // "debit" or "credit"
    val merchantName: String?,
    val upiId: String?,
    val referenceId: String?,
    val confidence: Double
)

object SmsParser {
    private val AMOUNT_PATTERN = Pattern.compile("(?i)(?:rs\\.?|inr|₹)\\s*([\\d,]+\\.?\\d*)")
    private val DEBIT_KEYWORDS = listOf("debited", "sent", "paid", "payment of")
    private val CREDIT_KEYWORDS = listOf("credited", "received")
    
    fun parse(rawSms: String): ParsedSms? {
        val lowerSms = rawSms.lowercase()
        
        var type: String? = null
        if (DEBIT_KEYWORDS.any { lowerSms.contains(it) }) {
            type = "debit"
        } else if (CREDIT_KEYWORDS.any { lowerSms.contains(it) }) {
            type = "credit"
        }
        
        if (type == null) return null
        
        val amountMatcher = AMOUNT_PATTERN.matcher(rawSms)
        if (!amountMatcher.find()) return null
        
        val amountStr = amountMatcher.group(1)?.replace(",", "") ?: return null
        val amountPaise = (amountStr.toDouble() * 100).toLong()
        
        // Return a simplified ParsedSms (In production, parse the rest)
        return ParsedSms(
            amount = amountPaise,
            type = type,
            merchantName = null,
            upiId = null,
            referenceId = null,
            confidence = 0.5
        )
    }
}

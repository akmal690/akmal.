package com.example.fraudverification;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
public class FraudVerificationController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @PostMapping("/api/verify_order_java")
    public Map<String, Object> verifyOrder(@RequestBody Map<String, Object> payload) {
        double typingSpeed = Double.parseDouble(payload.get("typing_speed").toString());
        double timeOnPage = Double.parseDouble(payload.get("time_on_page").toString());
        String paymentType = payload.get("payment_type").toString();

        // Prepare request to Python verification API
        RestTemplate restTemplate = new RestTemplate();
        Map<String, Object> reqBody = Map.of(
            "typing_speed", typingSpeed,
            "time_on_page", timeOnPage,
            "payment_type", paymentType,
            "user_id", payload.get("user_id").toString()
        );
        String url = "http://localhost:5000/verify";
        @SuppressWarnings("unchecked")
        Map<String, String> response = restTemplate.postForObject(url, reqBody, Map.class);

        String decision = response.get("decision");

        // Log the verification result into MySQL using JdbcTemplate
        jdbcTemplate.update(
            "INSERT INTO verification_logs (user_id, typing_speed, time_on_page, payment_type, verification_result, timestamp) VALUES (?, ?, ?, ?, ?, NOW())",
            payload.get("user_id").toString(), typingSpeed, timeOnPage, paymentType, decision
        );

        return Map.of("decision", decision);
    }
}
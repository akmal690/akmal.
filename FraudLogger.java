// FraudLogger.java (MySQL Integration)
import java.sql.*;

public class FraudLogger {
    private static final String URL = "jdbc:mysql://localhost:3306/shop_db";
    private static final String USER = "root";
    private static final String PASS = "";

    public static void logFraud(String userId, String reason, String context) {
        String sql = "INSERT INTO fraud_attempts (user_id, reason, context) VALUES (?, ?, ?)";
        
        try (Connection conn = DriverManager.getConnection(URL, USER, PASS);
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setString(1, userId);
            pstmt.setString(2, reason);
            pstmt.setString(3, context);
            pstmt.executeUpdate();
            
        } catch (SQLException e) {
            System.err.println("Fraud logging failed: " + e.getMessage());
        }
    }
}

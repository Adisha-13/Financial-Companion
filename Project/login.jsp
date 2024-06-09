<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.io.*,java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
  <title>Login Result</title>
</head>
<body>
  <%
    String username = request.getParameter("username");
    String password = request.getParameter("password");

    try {
      // Loading drivers for MySQL (Consider using a connection pool)
      Class.forName("com.mysql.jdbc.Driver");

      // Creating connection with the database
      try (Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/gitam", "root", "")) {
        String redirectUrl = "";

        String query = "SELECT * FROM finance WHERE uid = ? AND pass = ?";
        PreparedStatement ps = con.prepareStatement(query);
        ps.setString(1, username);
        ps.setString(2, password);

        ResultSet rs = ps.executeQuery();

          redirectUrl = "homepage.html";


          if (rs.next()) {
            redirectUrl = "homepage.html";
          } else {
            out.println("Invalid username or password!");
            out.println("<p>You will be redirected to the login page shortly...</p>");
            out.println("<script>setTimeout(function(){ window.location.href = 'login.html'; }, 3000);</script>");
          }
        

        // Redirect if a valid URL is found
        if (!redirectUrl.isEmpty()) {
          response.sendRedirect(redirectUrl);
        }
      }
    } catch (Exception se) {
      // Log the exception for debugging but don't print details to user
      se.printStackTrace();
      out.println("An error occurred. Please try again later.");
      out.println("<p>You will be redirected to the login page shortly...</p>");
      out.println("<script>setTimeout(function(){ window.location.href = 'login.html'; }, 3000);</script>");
    }
  %>
</body>
</html>

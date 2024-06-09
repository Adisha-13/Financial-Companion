<%@ page import="java.sql.*" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page errorPage="error.jsp" %>
<%
    String fn = request.getParameter("first");
    String ln = request.getParameter("last");
    String em = request.getParameter("email");
    String uid = request.getParameter("uid");
    String pass = request.getParameter("password");
    String cpass = request.getParameter("confirm");
    String mob = request.getParameter("mobile");
    String tableName = "finance"; // Always use 'finance' table
    boolean success = false;

    if (uid == null || pass == null || cpass == null ||!pass.equals(cpass)) {
        out.println("Password and Confirm Password must match!");
        return;
    }

    try {
        Class.forName("com.mysql.jdbc.Driver");
        try (Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/gitam", "root", "")) {
            String query = "INSERT INTO " + tableName + " VALUES (?,?,?,?,?,?,?)";
            try (PreparedStatement ps = con.prepareStatement(query)) {
                ps.setString(1, fn);
                ps.setString(2, ln);
                ps.setString(3, em);
                ps.setString(4, uid);
                ps.setString(5, pass);
                ps.setString(6, cpass);
                ps.setString(7, mob);
                int i = ps.executeUpdate();
                success = (i > 0);
            }
        }
    } catch (Exception se) {
        se.printStackTrace();
    }

    if (success) {
        out.println("You are successfully registered! Redirecting to login page...");
        response.setHeader("Refresh", "3; URL=login.html");
    } else {
        out.println("Registration failed! Please try again.");
    }
%>
// Buggy Example for ShadowCode Demo
const API_KEY = "ak_test_51MzByuSJRpG7zZzZzZzZzZzZzZzZzZz"; // Hardcoded Secret

function getUserData(userId) {
    // SQL Injection Vulnerability
    const query = "SELECT * FROM users WHERE id = " + userId;
    db.execute(query); 
}

function processInput(data) {
    // Unsafe Eval
    eval(data);
}

const db_password = "super_secret_password_123"; // Another secret

console.log("App started...");

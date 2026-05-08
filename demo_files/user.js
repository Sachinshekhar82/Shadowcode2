// User Configuration - Demo Credentials
const credentials = {
    username: "admin",
    password: "admin123" // HIGH RISK: Hardcoded plain-text password
};

function login(user, pass) {
    if (user === credentials.username && pass === credentials.password) {
        console.log("Login successful!");
        return true;
    }
    return false;
}

module.exports = { login };

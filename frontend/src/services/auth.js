import api from "./makeRequestWithAuth";
import { useNavigate } from "react-router-dom";


const API_BASE_URL = import.meta.env.VITE_API_BASE;

// attempts to register user with username, email and password
export async function register(username, email, password, passwordConfirmation, navigate) {
  if (password !== passwordConfirmation) {
    console.log('password and password confirmation do not match.');
    return false;
  }

  if (username && password && email) {

    try {
      // tries to register user
      const response = await api.post("/accounts/register/", {
        username: username,
        email: email,
        password: password,
        passwordConfirmation: passwordConfirmation
      });
      console.log(response);
      // redirects user to login page
      navigate("/login");
    } catch (error) {
      // handles exception
      console.error("Registration failed:", error);
      throw error;
    }

  } else {
    console.log('All form fields must be filled in.');
    return false;
  }
}

// attempts to log user in with username and password
export async function login(username, password, navigate) {
  // authenticates user
  try {
    // fetches refresh and acces tokens
    const response = await api.post("/accounts/api/token/", {
      username: username,
      password: password
    });
    // saves username and tokens to local storage
    localStorage.setItem("user", username);
    localStorage.setItem("accessToken", response.data.access);
    localStorage.setItem("refreshToken", response.data.refresh);

    // redirects user to home page
    navigate("/");
  } catch (error) {
    // handle exception
    console.error("Login failed:", error);
    throw error;
  }

  // gets relevant user data
  try {
    // fetches user data
    const response = await api.get("/accounts/me/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
      },
    });
    // saves user id to local storage
    localStorage.setItem("userId", response.data.id);
  } catch (error) {
    console.error("Fetch current user data failed:", error);
    throw error;
  }
}
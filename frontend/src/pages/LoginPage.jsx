// layout
import LoginRegisterLayout from "../layouts/LoginRegisterLayout";
// components
import { Form, FormField } from "../components/Form";
// services
import { login } from "../services/auth";
// hooks
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";


export default function LoginPage() {

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  
  const navigate = useNavigate();

  const fields = [
    { label: "Username", type: "text", placeholder: "username", onChange: (event) => {setUsername(event.target.value)} },
    { label: "Password", type: "password", placeholder: "password", onChange: (event) => {setPassword(event.target.value)} },
  ];

  return (
    <>
      <LoginRegisterLayout footer="0-0">
        {/* Login form */}
        <Form
        title="Login"
        fields={fields}
        onSubmit={() => login(username, password, navigate)}
        buttonText="Login"
        />
        <p className="text-xs font-light mt-2">Don't have an account? <Link to="/register" className="link">Register</Link></p>
      </LoginRegisterLayout>
    </>
  );
}
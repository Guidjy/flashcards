// layout
import LoginRegisterLayout from "../layouts/LoginRegisterLayout";
// components
import { Form, FormField } from "../components/Form";
// services
import { register } from "../services/auth";
// hooks
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";


export default function RegisterPage() {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");

  const navigate = useNavigate();

  const fields = [
    { label: "Username", type: "text", placeholder: "username", onChange: (event) => {setUsername(event.target.value)} },
    { label: "Email", type: "email", placeholder: "example@email.com", onChange: (event) => {setEmail(event.target.value)} },
    { label: "Password", type: "password", placeholder: "password", onChange: (event) => {setPassword(event.target.value)} },
    { label: "Confirm Password", type: "password", placeholder: "password", onChange: (event) => {setPasswordConfirmation(event.target.value)} },
  ];

  return (
    <>
      <LoginRegisterLayout>
        {/* Login form */}
        <Form
        title="Register"
        fields={fields}
        onSubmit={() => register(username, email, password, passwordConfirmation, navigate)}
        buttonText="Register"
        />
        <p className="text-xs font-light mt-2">Already have an account? <Link to="/login" className="link">Sign in</Link></p>
      </LoginRegisterLayout>
    </>
  );
}
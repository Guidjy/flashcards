import { useState } from "react"
import { Link, useNavigate } from "react-router-dom";
import { login, logout, register } from "../services/auth";


export default function Auth() {
  
  const [authState, setAuthState] = useState('login');

  return (
    <>
      <div className="w-full h-screen flex justify-center items-center">
        <div className="p-5 rounded-2xl w-5/6 md:w-3/4 lg:w-1/2 xl:w-1/3">
          {authState === 'login' ? (
            <LoginForm setAuthState={setAuthState}  />
          ) : (
            <RegisterForm setAuthState={setAuthState} />
          )}
        </div>
      </div>
    </>
  )
}


function FormTextField({ id, label, placeholder, onFormEdit }) {
  return (
    <>
      <label className="label">{label}</label>
      <input id={id} onChange={(event) => onFormEdit(event.target.value)} type="text" className="input w-full" placeholder={placeholder} />
    </>
  )
}


function LoginForm({ setAuthState }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  async function handleFormSubmit() {
    const result = login(username, password);
    if (result) {
      navigate('/');
    } else {
      console.log('Login failed');
    }
    console.log(result);
  }

  return (
    <>
      <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-full border p-4">
        <legend className="fieldset-legend">Login</legend>
        <FormTextField id='username' onFormEdit={setUsername} label={'Username'} placeholder={'Username'} />
        <FormTextField id='password' onFormEdit={setPassword} label={'Password'} placeholder={'Password'} />

        <button onClick={handleFormSubmit} className="btn btn-primary my-3">Login</button>
        <div className="flex" >
          <p className="me-1">Don't have an account?</p>
          <div onClick={() => setAuthState('register')} className="underline hover:text-primary">Register</div>
        </div>
      </fieldset>
    </>
  )
}


function RegisterForm({ setAuthState }) {

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');

  async function handleFormSubmit() {
    const result = register(username, email, password, passwordConfirmation);
    //console.log(result);
  }

  return (
    <>
      <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-full border p-4">
        <legend className="fieldset-legend">Register</legend>
        <FormTextField id='username' onFormEdit={setUsername} label={'Username'} placeholder={'Username'} />
        <FormTextField id='email' onFormEdit={setEmail} label={'email'} placeholder={'example@email.com'} />
        <FormTextField id='password' onFormEdit={setPassword} label={'Password'} placeholder={'Password'} />
        <FormTextField id='password-confirmation' onFormEdit={setPasswordConfirmation} label={'Password Confirmation'} placeholder={'Type your password again'} />

        <button onClick={handleFormSubmit} className="btn btn-primary my-3">Register</button>
        <div className="flex" >
          <p className="me-1">Already have an account?</p>
          <div onClick={() => setAuthState('login')} className="underline hover:text-primary">Login</div>
        </div>
      </fieldset>
    </>
  )
}
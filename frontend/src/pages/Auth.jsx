import { useState } from "react"
import { Link } from "react-router-dom";

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


function FormTextField({ label, placeholder }) {
  return (
    <>
      <label className="label">{label}</label>
      <input type="text" className="input w-full" placeholder={placeholder} />
    </>
    
  )
}


function LoginForm({ setAuthState }) {
  return (
    <>
      <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-full border p-4">
        <legend className="fieldset-legend">Login</legend>
        <FormTextField label={'Username'} placeholder={'Username'} />
        <FormTextField label={'Password'} placeholder={'Password'} />

        <button className="btn btn-primary my-3">Login</button>
        <div className="flex" >
          <p className="me-1">Don't have an account?</p>
          <div onClick={() => setAuthState('register')} className="underline hover:text-primary">Register</div>
        </div>
      </fieldset>
    </>
  )
}


function RegisterForm({ setAuthState }) {
  return (
    <>
      <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-full border p-4">
        <legend className="fieldset-legend">Register</legend>
        <FormTextField label={'Username'} placeholder={'Username'} />
        <FormTextField label={'email'} placeholder={'example@email.com'} />
        <FormTextField label={'Password'} placeholder={'Password'} />
        <FormTextField label={'Password Confirmation'} placeholder={'Type your password again'} />

        <button className="btn btn-primary my-3">Register</button>
        <div className="flex" >
          <p className="me-1">Already have an account?</p>
          <div onClick={() => setAuthState('login')} className="underline hover:text-primary">Login</div>
        </div>
      </fieldset>
    </>
  )
}
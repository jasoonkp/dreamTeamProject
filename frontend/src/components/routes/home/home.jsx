import React from 'react';
import { SignInForm } from "../../signInForm/signInForm";
import { SignUpForm } from "../../signUpForm/signUpForm";
import "./home.styles.scss";

export const Home = () => {
  return (
    <div className="home-container">
      <div className="background-animation"></div>
      <div className="content">
        <div className="title-container">
          <h1>Teacher's Assistant</h1>
          <p className="subtitle">
            Your best friend to get you through your class and your homework.
          </p>
        </div>
        <div className="authentication-container">
          <SignInForm />
          <SignUpForm />
        </div>
      </div>
    </div>
  );
};

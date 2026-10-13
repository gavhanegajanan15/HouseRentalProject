import { initializeApp } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js";

import {
    getAuth,
    RecaptchaVerifier,
    signInWithPhoneNumber
} from "https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js";


const firebaseConfig = {

    apiKey: "AIzaSyB6Vo3aXOLKBOdN7zdnaCXI86z5XBcbAKk",

    authDomain: "house-rental-portal-20b33.firebaseapp.com",

    projectId: "house-rental-portal-20b33",

    storageBucket: "house-rental-portal-20b33.firebasestorage.app",

    messagingSenderId: "143304544932",

    appId: "1:143304544932:web:a09f88da4c9f59e3218c31",

    measurementId: "G-G71CF6LGPF"

};


const app = initializeApp(firebaseConfig);

const auth = getAuth(app);


// Make Firebase available to register.js

window.auth = auth;

window.RecaptchaVerifier = RecaptchaVerifier;

window.signInWithPhoneNumber = signInWithPhoneNumber;
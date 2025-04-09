// login_script.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-app.js";
import {
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  FacebookAuthProvider,
  OAuthProvider
} from "https://www.gstatic.com/firebasejs/11.6.0/firebase-auth.js";

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyD_qC7Y_jH50ysjrsfqTG6mT5728_EBons",
  authDomain: "ai-study-buddy-b5846.firebaseapp.com",
  projectId: "ai-study-buddy-b5846",
  storageBucket: "ai-study-buddy-b5846.appspot.com",
  messagingSenderId: "366005568947",
  appId: "1:366005568947:web:3d512c2c88cce6987ef7c6"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// 🔁 After login, redirect here:
const redirectUrl = "https://calmoneyedu.github.io/unnamed/";

// Google Sign-In
document.querySelector('.google-btn')?.addEventListener('click', () => {
  const provider = new GoogleAuthProvider();
  signInWithPopup(auth, provider)
    .then(() => {
      window.location.href = redirectUrl;
    })
    .catch(error => {
      console.error(error);
      alert(error.message);
    });
});

// Microsoft Sign-In
document.querySelector('.microsoft-btn')?.addEventListener('click', () => {
  const provider = new OAuthProvider('microsoft.com');
  signInWithPopup(auth, provider)
    .then(() => {
      window.location.href = redirectUrl;
    })
    .catch(error => {
      console.error(error);
      alert(error.message);
    });
});

// Facebook Sign-In
document.querySelector('.facebook-btn')?.addEventListener('click', () => {
  const provider = new FacebookAuthProvider();
  signInWithPopup(auth, provider)
    .then(() => {
      window.location.href = redirectUrl;
    })
    .catch(error => {
      console.error(error);
      alert(error.message);
    });
});
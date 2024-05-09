// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDETzhdmmHaizxR48A5jar8dAZs4w_uj7M",
  authDomain: "grocerite-f39ad.firebaseapp.com",
  projectId: "grocerite-f39ad",
  storageBucket: "grocerite-f39ad.appspot.com",
  messagingSenderId: "695035891584",
  appId: "1:695035891584:web:1be1b10d417047e4ab7b65",
  measurementId: "G-PXMZLJ7DT7"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);
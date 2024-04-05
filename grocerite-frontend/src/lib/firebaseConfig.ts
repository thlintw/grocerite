// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBcR-BZoRByg_LFQ9JhsgtU5XvKyOPkooc",
  authDomain: "quixotic-vent-418808.firebaseapp.com",
  projectId: "quixotic-vent-418808",
  storageBucket: "quixotic-vent-418808.appspot.com",
  messagingSenderId: "776169597383",
  appId: "1:776169597383:web:cd1477d3558dc20fdc91e2",
  measurementId: "G-2HS9ECY1TX"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
export const auth = getAuth(app);
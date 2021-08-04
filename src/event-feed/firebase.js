import firebase from 'firebase'

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCgpVK6yw3tqcGDM8XlPHVcT8q_5gj0n0A",
    authDomain: "pactimeline.firebaseapp.com",
    projectId: "pactimeline",
    storageBucket: "pactimeline.appspot.com",
    messagingSenderId: "696595680666",
    appId: "1:696595680666:web:1a574bafee3c75077bbe23",
    measurementId: "G-LVXD6HG7KD"
  };

const firebaseApp = firebase.initializeApp(firebaseConfig)

const db = firebaseApp.firestore()
db.settings({timestampsInSnapshots: true})

export default db
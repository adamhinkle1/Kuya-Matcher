import React, { useState,useEffect } from 'react';
import './App.css';
import axios from 'axios'
import Home from './home/Home'
import Login from './login/Login'
import Logout from './login/Logout'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import AdingQuestionairre from './applications/ading/AdingQuestionairre';
import AteQuestionairre from './applications/ate-kuya/AteQuestionairre';
import Events from './event-feed/Events'
import {useStateValue} from './Context/StateProvider'
import {AdminStateValue} from './Context/AdminProvider'
import {QuestionStateValue} from './Context/QuestionProvider'
import {actionTypes} from './Context/reducer'

function App() {

  const [{user}, dispatch] = useStateValue()
  const [isAdmin, setIsAdmin] = AdminStateValue()
  const [big,setBig] = useState()
  const [little,setLittle] = useState()
  const [q, setQSV] = QuestionStateValue()
  
  // get question sets 
  useEffect(async() => {
    await axios.get('/main/question_set/big' )
    .then(function (response) {
        setBig(response.data)
      })
      .catch((error) => {
        console.log(error)
      });
  },[]);
  useEffect(async() => {
    await axios.get('/main/question_set/little')
    .then(function (response) {
        setLittle(response.data)
      })
      .catch((error) => {
        console.log(error)
      });
  },[]);

  //update context for questions
  useEffect(()=>{
    setQSV({
      type: actionTypes.SET_Q,
      q: {big: big, little: little}
    })
  },[big,little])

  //get user data and post to context
  useEffect(async() => {
    await axios.get('/user/info')
    .then(function (response) {
      dispatch({
        type: actionTypes.SET_USER,
        user: response.data,  
      })
    })
    .catch((error) => {
      console.log(error)
    })
  },[]);

  //check if user is an admin, create context
  useEffect(async() => {
    await axios.get('/user/is_admin')
    .then(function (response) {
      console.log(response.data)
      if (response.data){
        setIsAdmin({
          type: actionTypes.SET_ISADMIN,
          isAdmin: true,  
        })
      }
      else{
        setIsAdmin({
          type: actionTypes.SET_ISADMIN,
          isAdmin: false,  
        })
      }
    })
    .catch((error) => {
      console.log(error)
    })
  },[user])

  console.log(isAdmin)

  return (
    <>
    <Router>
      <Switch>
        <Route path='/' exact component={Home} />
        <Route path='/login' component={Login} />
        <Route path='/logout' component={Logout} />
        <Route path='/ading-questions' component={AdingQuestionairre} />
        <Route path='/ate-questions' component={AteQuestionairre} />
        <Route path='/events' component={Events} />
      </Switch>
    </Router>
  </>
  );
}

export default App;

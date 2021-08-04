import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { AppBar, IconButton, Collapse, Toolbar } from '@material-ui/core';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { Link as Scroll } from 'react-scroll';
import Navbar from './Navbar';
import './Navbar.css'
const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    fontFamily: 'Nunito',
  },
  appbar: {
    display: 'flex',
    marginTop: '10px',
    background: 'none',
  },
  appbarWrapper: {
    width: '100%',
    margin: '0 auto',
    textAlign: 'center'
  }, 
  colorText: {
    color: 'white',
    fontSize: '4rem',
  },
  appbarTitle: {
    flexGrow: '1',
    color: '#ECAA00',
    fontSize: '3rem',
    textShadow: '5px 5px 15px rgba(0, 0, 0, 1)',
},
  colorText: {
    textShadow: '5px 5px 15px rgba(0, 0, 0, 1)',
    color: 'white',
    fontSize: '4.5rem',
},
  container: {
    marginTop: '75vh',
    alignItems: 'center',
},
  title: {
    color: 'white',
},
  goDown: {
      color: 'whitesmoke',
      fontSize: '6rem',
      transition: 'transform 0.5s ease',
      '&:hover': {
        backgroundColor: 'none',
        transform: 'scale(1.1)',
        transform: 'rotate(-360deg)',
        textShadow: '2px 2px 50px white',
    },
},
}));
export default function Header() {
  const classes = useStyles();
  const [checked, setChecked] = useState(false);
  useEffect(() => {
    setChecked(true)
  }, [])
  return (
    <div className={classes.root} id="header">
      <AppBar className={classes.appbar} elevation={0}>
        <Toolbar className={classes.appbarWrapper}>
        <Navbar />
          <h1 className={classes.appbarTitle}>
            <span className={classes.colorText}>P</span>
            ilipino 
            <span className={classes.colorText}> A</span>
            merican 
            <span className={classes.colorText}> C</span>
            oalition
          </h1>
        </Toolbar>
      </AppBar>

      <Collapse
        in={checked}
        {...(checked ? { timeout: 300 } : {})}
        collapsedHeight={200}
      >
        <div className={classes.container}>
          <Scroll to="place-to-visit" smooth={true}>
            <IconButton  style={{ backgroundColor: 'none' }}>
              <ExpandMoreIcon className={classes.goDown} />
            </IconButton>
          </Scroll>
        </div>
      </Collapse>
    </div>
  );
}

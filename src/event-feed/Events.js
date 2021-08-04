import React from 'react'
import {makeStyles} from '@material-ui/core/styles'
import {CssBaseline} from '@material-ui/core'
import Timeline from './Timeline'
import Header from '../applications/Header'

const useStyles = makeStyles ((theme) => ({
    root: {
      backgroundImage: `url(${process.env.PUBLIC_URL + '/img/blue.jpg'})`,
      backgroundRepeat: 'no-repeat',
      backgroundSize: 'cover',
      minHeight: '100vh',
    },
    pageContent: {
      margin: theme.spacing(7),
      padding: theme.spacing(2),
    },
  }))


function Events() {
    const classes = useStyles()
    return (
        <div className={classes.root}>
            <CssBaseline />
            <Header title = "PAC Events"/>
            <Timeline />
        </div>
    )
}

export default Events

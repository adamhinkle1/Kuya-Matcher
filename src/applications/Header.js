import React from 'react'
import {makeStyles} from '@material-ui/core/styles'

import Navbar from './Navbar'

const useStyles = makeStyles((theme) => ({
    root:{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'white',
        boxShadow: '5px 5px 10px 5px rgba(0,0,0,.2)',
        position: 'sticky',
    },
    icon: {
        marginTop: '15px',
        marginLeft: '5px',

    },
    title: {
        textAlign: 'center',
        flexGrow: '.95',
        color: 'black',
        textShadow: '4px 4px 5px rgba(0, 0, 0, .3)',
        fontSize: '3rem',
        
    },
}))
function Header({title}) {
    const classes = useStyles()
    return (
        <div className = {classes.root}>
            <div className= {classes.icon} >
                <Navbar />
            </div>
            <h1 className={classes.title}>
                {title}
            </h1>
        </div>
        
    )
}

export default Header
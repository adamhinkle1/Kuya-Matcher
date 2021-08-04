import React from 'react'
import {makeStyles} from '@material-ui/core/styles'
import {CssBaseline} from '@material-ui/core'
import Header from './Header'
import PlaceToVisit from './PlaceToVisit';

const useStyles = makeStyles((theme) => ({
    root: {
        minHeight: '100vh',
        backgroundImage: `url(${process.env.PUBLIC_URL + '/img/b1.png'})`,
        backgroundRepeat: 'repeat',
        backgroundSize: 'cover',
    },
}))
function Home() {
    const classes = useStyles()
    return (
        <div className={classes.root}>
            <CssBaseline />
            <Header />
            <PlaceToVisit />
        </div>
    )
}  
export default Home
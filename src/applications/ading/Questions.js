import React from 'react'
import {makeStyles} from '@material-ui/core/styles'
import ApplicationForm from '../form/ApplicationForm'
import {QuestionStateValue} from '../../Context/QuestionProvider'

const useStyles = makeStyles((theme) => ({
    root: {
        height: '87vh',
        justifyContent: 'center',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
    },
    container: {
        overflowY: 'auto',
        backgroundColor: 'whitesmoke',
        width: '150vh',
        minHeight:'87vh',
        boxShadow: '3px 3px 10px 1px rgba(0,0,0,.5)',
        height: 'auto',
        display: 'block',
        marginLeft: 'auto',
        marginRight: 'auto',
    },
    questions: {
        padding: '15px 25px',
        display: 'flex',
        flexDirection: 'column',
    },
}))
function Questions() {
    const [{q}, setQ] = QuestionStateValue()
    const classes = useStyles()
    return (
        <div className={classes.root}>
            <div className = {classes.container}>
                <div className = {classes.questions}>
                    <ApplicationForm type='little'  mc={q.little}/>
                </div>
            </div>
        </div>
    )
}

export default Questions

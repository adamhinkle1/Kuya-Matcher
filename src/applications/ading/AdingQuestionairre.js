import {makeStyles} from '@material-ui/core/styles'
import {CssBaseline} from '@material-ui/core'
import Header from '../Header'
import Questions from './Questions'
const useStyles = makeStyles ((theme) => ({
  root: {
    backgroundColor: '#CAEBF2',
    minHeight: '100vh',
  },
}))
function AdingQuestionairre() {
  const classes = useStyles()
  return (
    <div className={classes.root}>
      <CssBaseline />
      <Header title="Ading Application"/>
      <Questions />
    </div>
  );
}

export default AdingQuestionairre;

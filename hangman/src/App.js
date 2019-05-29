import React from 'react';
import clsx from 'clsx';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

import './App.css';
import { GetFetch } from './hooks';
import Message from './components/Message';
import CharPrompt from './components/CharPrompt';
import Screen from './components/Screen';

const useStyles = makeStyles(theme => ({
  '@global': {
    body: {
      backgroundColor: theme.palette.common.white,
    },
  },
  container: {
    paddingTop: theme.spacing(8),
    paddingBottom: theme.spacing(4),
  },
  paper: {
    marginTop: theme.spacing(2),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  messageHeight: {
    height: 125,
  },
  lettersHeight: {
    height: 100,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function App() {
  const classes = useStyles();
  const messagePaper = clsx(classes.paper, classes.messageHeight);
  const lettersPaper = clsx(classes.paper, classes.lettersHeight);
  const initialState = {
    'life': 5,
    'spaces': '',
    'guesses': '',
    'alert': '',
    'token': '',
  }

  let [data, updateData, fetchStart] = GetFetch('http://localhost:5000/api/v1/start', initialState);

  const restartGame = () => {
    updateData(initialState);
    fetchStart();
  }

  return (
    <Container component="main" maxWidth="xs" className={classes.container}>
      <CssBaseline />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          hangman
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Paper className={messagePaper}>
              <Message message={data.alert} />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper className={lettersPaper}>
              <Screen data={data}/>
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <CharPrompt data={data} update={updateData} restart={restartGame}/>
          </Grid>
        </Grid>
      </div>
    </Container>
  );
}

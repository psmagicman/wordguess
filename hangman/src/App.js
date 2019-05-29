import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Dialog from '@material-ui/core/Dialog';

import './App.css';
import { GetFetch } from './hooks';
import { gameFlags } from './enums';
import Message from './components/Message';
import CharPrompt from './components/CharPrompt';
import Screen from './components/Screen';
import RestartButton from './components/RestartButton';
import Score from './components/Score';

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
  const [open, setOpen] = useState(false);
  const messagePaper = clsx(classes.paper, classes.messageHeight);
  const lettersPaper = clsx(classes.paper, classes.lettersHeight);
  const initialState = {
    'life': 5,
    'spaces': '_',
    'guesses': '',
    'alert': '',
    'token': '',
    'status': 0,
    'stoken': '',
  }

  let [data, updateData, fetchStart] = GetFetch('/api/v1/start', initialState);

  const restartGame = () => {
    updateData(initialState);
    fetchStart();
  }

  function handleOpen() {
    setOpen(true);
  }

  function handleClose() {
    setOpen(false);
    setTimeout(() => {
      restartGame();
    }, 3000);
  }

  useEffect(() => {
    if (data.status === gameFlags.WIN) {
      setTimeout(() => {
        handleOpen();
      }, 2000);
    }
  }, [data.status])

  return (
    <Container component="main" maxWidth="xs" className={classes.container}>
      <CssBaseline />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          hangman
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <RestartButton onClick={restartGame} />
          </Grid>
          <Grid item xs={12}>
            <Paper className={messagePaper}>
              <Message message={data.alert} />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper className={lettersPaper}>
              <Screen data={data} />
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <CharPrompt 
              data={data} 
              update={updateData} 
              restart={restartGame} 
              status={data.status} />
          </Grid>
        </Grid>
        <Dialog
          open={open}
          onClose={handleClose}
        >
          <Score handleClose={handleClose} data={data} update={updateData} />
        </Dialog>
      </div>
    </Container>

  );
}

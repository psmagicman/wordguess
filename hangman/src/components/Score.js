import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';
import { makeStyles } from '@material-ui/core/styles';
import Snackbar from '@material-ui/core/Snackbar';

import { PostFetch } from '../hooks';

const useStyles = makeStyles(theme => ({
  error: {
    backgroundColor: theme.palette.error.dark,
  },
  message: {
    display: 'flex',
    alignItems: 'center',
  },
  icon: {
    fontSize: 20,
  },
  iconVariant: {
    opacity: 0.9,
    marginRight: theme.spacing(1),
  },
}))

export default function Score(props) {
  const [name, setName] = useState('');
  const [snackOpen, setSnackOpen] = useState(false);
  let stoken = props.data.hasOwnProperty('stoken') ? props.data.stoken : '';

  const classes = useStyles();

  const sendScore = PostFetch('/api/v1/score', props.update);

  const handleOpenSnackBar = () => {
    setSnackOpen(true);
  }

  const handleCloseSnackBar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackOpen(false);
  }

  const onEnter = (e) => {
    // Return key
    if (e.keyCode === 13) {
      saveScore();
    }
  }

  const saveScore = () => {
    if (name || stoken) {
      sendScore({'name': name, 'stoken': stoken});
      setName('');
      props.handleClose();
    } else {
      handleOpenSnackBar();
    }
  }

  return (
    <div className="">
      <Snackbar
        className={classes.margin}
        variant="error"
        autoHideDuration={3000}
        open={snackOpen}
        onClose={handleCloseSnackBar}
        message={
          <span id="score-snackbar" className={classes.message}>
            No name or score found.
          </span>
        }
      />
      <DialogTitle id="score-dialog-title">Save score</DialogTitle>
      <DialogContent>
        <TextField
            name="nameField"
            variant="outlined"
            fullWidth
            id="nameField"
            label="Name"
            onKeyDown={onEnter}
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
      </DialogContent>
      <DialogActions>
          <Button
            type="button"
            variant="contained"
            color="secondary"
            onClick={props.handleClose}
          >
            Cancel
          </Button>
          <Button 
            type="button"
            variant="contained"
            color="primary"
            onClick={saveScore}
          >
            Save score
          </Button>
      </DialogActions>
    </div>
  );
}
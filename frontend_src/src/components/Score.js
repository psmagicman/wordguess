import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
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
  const [snackErrorOpen, setSnackErrorOpen] = useState(false);
  const [snackSaveOpen, setSnackSaveOpen] = useState(false);
  let stoken = props.data.hasOwnProperty('stoken') ? props.data.stoken : '';
  let open = props.open;

  const classes = useStyles();

  const sendScore = PostFetch(process.env.REACT_APP_URL 
                        + '/api/v1/score', props.update);

  const handleOpenErrorSnackBar = () => {
    setSnackErrorOpen(true);
  }

  const handleCloseErrorSnackBar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackErrorOpen(false);
  }

  const handleOpenSaveSnackBar = () => {
    setSnackSaveOpen(true);
  }

  const handleCloseSaveSnackBar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackSaveOpen(false);
  }

  const onEnter = (e) => {
    // Return key
    if (e.keyCode === 13) {
      saveScore();
    }
  }

  const saveScore = () => {
    if (name.length > 0 && stoken.length > 0) {
      sendScore({'name': name, 'stoken': stoken});
      setName('');
      handleOpenSaveSnackBar();
      props.handleClose();
    } else {
      handleOpenErrorSnackBar();
    }
  }

  return (
    <div className="">
      <Snackbar
        className={classes.margin}
        autoHideDuration={2000}
        open={snackSaveOpen}
        onClose={handleCloseSaveSnackBar}
        message={
          <span id="score-save-snackbar" className={classes.message}>
            Name and score saved.
          </span>
        }
      />
      <Snackbar
        className={classes.margin}
        autoHideDuration={1000}
        open={snackErrorOpen}
        onClose={handleCloseErrorSnackBar}
        message={
          <span id="score-error-snackbar" className={classes.message}>
            No name or score found.
          </span>
        }
      />
      <Dialog
        open={open}
        onClose={props.handleClose}
      >
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
      </Dialog>
    </div>
  );
}
import React, { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';

import { PostFetch } from '../hooks';
import { gameFlags } from '../enums';

export default function CharPrompt(props) {
  const [char, setChar] = useState('');
  const [disable, setDisable] = useState(false);
  
  let token = props.data.hasOwnProperty('token') ? props.data.token : '';

  const sendChar = PostFetch('http://localhost:5000/api/v1/word', props.update)
  const onEnter = (e) => {
    // Return key
    if (e.keyCode === 13) {
      sendData();
    }
  }

  const sendData = () => {
    sendChar({'char': char, 'token': token});
    setChar('');
  }

  useEffect(() => {
    if (props.status === gameFlags.START) {
      setChar('');
      setDisable(false);
    } else if (props.status > gameFlags.PROGRESS) {
      setDisable(true);
      setChar('');
    }
  }, [props.status]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={6}>
        <TextField
          name="charField"
          variant="outlined"
          fullWidth
          id="charField"
          label="Character"
          autoFocus
          value={char}
          disabled={disable}
          onKeyDown={onEnter}
          onChange={(e) => setChar(e.target.value)}
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <Button
          type="button"
          fullWidth
          variant="contained"
          color="primary"
          disabled={disable}
          onClick={sendData}
        >
          Submit
        </Button>
      </Grid>
    </Grid>
  );
}

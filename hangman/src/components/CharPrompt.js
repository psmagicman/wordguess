import React, { useState, useEffect } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';

import { PostFetch } from '../hooks';

export default function CharPrompt(props) {
  const [char, setChar] = useState('');
  const [token, setToken] = useState('');
  
  useEffect(() => {
    setToken(props.data.token);  
  }, [props.data.token]);
  
  const [res, caller] = PostFetch('http://localhost:5000/api/v1/word', char, token)

  const callerHandler = (char, token) => {
    caller(char, token)
  }

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={6}>
        <TextField
          name="charField"
          variant="outlined"
          required
          fullWidth
          id="charField"
          label="Character Field"
          autoFocus
          onChange={(e) => setChar(e.target.value)}
        />
      </Grid>
      <Grid item xs={12} sm={6}>
        <Button
          type="button"
          fullWidth
          variant="contained"
          color="primary"
          onClick={() => { callerHandler(char, token) }}
        >
          Submit
        </Button>
      </Grid>
    </Grid>
  );
}

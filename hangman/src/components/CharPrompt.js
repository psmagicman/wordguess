import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';

import { PostFetch } from '../hooks';

export default function CharPrompt(props) {
  const [char, setChar] = useState('');
  
  let token = props.data.token ? props.data.token : '';

  const sendChar = PostFetch('http://localhost:5000/api/v1/word', props.update)

  const restart = function() {
    props.restart();
    setChar('');
  }

  return (
    <div>
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
            value={char}
            onChange={(e) => setChar(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <Button
            type="button"
            fullWidth
            variant="contained"
            color="primary"
            onClick={() => { sendChar(char, token) }}
          >
            Submit
          </Button>
        </Grid>
      </Grid>
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Button
            type="button"
            fullWidth
            size="large"
            variant="contained"
            color="secondary"
            onClick={() => { restart() }}
          >
            Restart
          </Button>
        </Grid>
      </Grid>
    </div>
  );
}

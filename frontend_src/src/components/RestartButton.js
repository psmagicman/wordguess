import React from 'react';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';

export default function Restart(props) {

  const restart = function() {
    props.onClick();
  }

  return (
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
  );

}


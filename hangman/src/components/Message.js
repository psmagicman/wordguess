import React, { useState, useEffect } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

export default function Message(props) {
  const [alert, setAlert] = useState('...')

  if (props.message) {
    setAlert(props.message)
  }

  return (
    <Typography 
        component="p" 
        variant="h2" 
        color="textPrimary" 
        align="center" 
        gutterBottom>
      {alert}
    </Typography>
  );
}
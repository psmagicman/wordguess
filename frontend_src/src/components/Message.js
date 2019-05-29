import React from 'react';
import Typography from '@material-ui/core/Typography';

export default function Message(props) {
  
  const alert = props.message ? props.message : '...';

  return (
    <Typography 
        component="p" 
        variant="h6" 
        color="textPrimary" 
        align="center" 
        gutterBottom>
      {alert}
    </Typography>
  );
}
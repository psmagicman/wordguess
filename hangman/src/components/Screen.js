import React from 'react';
import Typography from '@material-ui/core/Typography';

export default function Screen(props) {

  function delimitGuesses(guessSequence) {
    return guessSequence.split('').join(', ');
  }

  function separateSpaces(spaceSequence) {
    return spaceSequence.split('').join(' ');
  }

  const life = props.data.life ? props.data.life : 5;
  const spaces = props.data.spaces ? separateSpaces(props.data.spaces) : '';
  const guesses = props.data.guesses ? delimitGuesses(props.data.guesses) : '';

  return (
    <div>
      <Typography component="p">
        Incorrect guesses remaining: {life}
      </Typography>
      <Typography component="p" variant="h6" align="center" gutterBottom>
        {spaces}
      </Typography>
      <Typography component="p">
        Current guesses: {guesses}
      </Typography>
    </div>
  );
};
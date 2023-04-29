import * as React from 'react';
import Home from './Home';
import Typography from "@mui/material/Typography";


export default function MyApp() {

  return (
    <>
      <Typography align="center" variant="h3" component="div" sx={{ flexGrow: 1 }}>
        Pynance
      </Typography>
      <Home/>
    </>

  );
}

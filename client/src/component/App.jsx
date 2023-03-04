import React from "react"; 

import { createTheme, ThemeProvider } from '@mui/material/styles';

import AppBar from "@mui/material/AppBar";
import Container from "@mui/material/Container"
import CssBaseline from "@mui/material/CssBaseline";
import Paper from "@mui/material/Paper";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

import Copyright from "./Copyright";
import XmlExporter from "./XmlExporter";

const theme = createTheme();

const App = () => {
  
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar
        position="absolute"
        sx={{ position: "relative" }}
      >
        <Toolbar>
          <Typography variant="h6">
            Rosetta
          </Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
        <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
          <XmlExporter />
        </Paper>
        <Copyright />
      </Container>
    </ThemeProvider>
  );
};

export default App;

import React, { useState, useEffect } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import placeholder from './components/placeholder.png';

const App = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#4caf50', // Green shade
      },
      secondary: {
        main: '#f44336', // Red shade
      },
    },
  });

  useEffect(() => {
    document.body.style.backgroundColor = darkMode ? '#121212' : '#f5f5f5';
  }, [darkMode]);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  const menuItems = ['Home', 'Other', 'Settings', 'Log Out'];

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static" color="inherit" elevation={0}>
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              onClick={toggleMenu}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              HealthBuddy
            </Typography>
            <IconButton color="inherit" onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>
        <Drawer anchor="left" open={isMenuOpen} onClose={toggleMenu}>
          <Box sx={{ width: 250 }}>
            <List>
              {menuItems.map((item, index) => (
                <ListItem button key={`${item}-${index}`}>
                  <ListItemText
                    primary={item}
                    style={{
                      color:
                        index === 2
                          ? theme.palette.primary.main
                          : index === menuItems.length - 1
                          ? theme.palette.secondary.main
                          : theme.palette.text.primary,
                    }}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            flexGrow: 0.3,
            padding: '0.3rem',
          }}
        >
          <Card sx={{ maxWidth: '90vw', maxHeight: '90vh' }}>
            <CardMedia
              component="img"
              height="100%"
              image={placeholder}
              alt="Sample"
            />
            <CardContent>
              {/* Additional content can be added here */}
            </CardContent>
          </Card>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;
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
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import placeholder from './components/placeholder2.png';
import './App.css';

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [themeProfile, setThemeProfile] = useState('tiramisu');

  useEffect(() => {
    document.body.className = `${darkMode ? 'dark-mode' : 'light-mode'} ${themeProfile}`;
  }, [darkMode, themeProfile]);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: getComputedStyle(document.documentElement).getPropertyValue('--primary-color').trim(),
      },
      background: {
        default: getComputedStyle(document.documentElement).getPropertyValue('--background-color').trim(),
        paper: getComputedStyle(document.documentElement).getPropertyValue('--box-background-color').trim(),
      },
      text: {
        primary: getComputedStyle(document.documentElement).getPropertyValue('--text-color').trim(),
      },
    },
    typography: {
      fontFamily: 'Poppins, sans-serif',
      allVariants: {
        textTransform: 'lowercase',
        fontWeight: 400,
      },
    },
  });

  const handleToggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleMenuToggle = () => {
    setMenuOpen(!menuOpen);
  };

  const handleThemeProfileChange = (event: SelectChangeEvent<string>) => {
    setThemeProfile(event.target.value);
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ flexGrow: 1, position: 'relative', minHeight: '100vh' }}>
        <AppBar position="fixed" color="inherit" sx={{ zIndex: 1400 }}>
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu" onClick={handleMenuToggle}>
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Health<span style={{ fontWeight: 'bold' }}>buddy</span>
            </Typography>
            <IconButton color="inherit" onClick={handleToggleDarkMode}>
              {darkMode ? <DarkModeIcon /> : <LightModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>
        {menuOpen && (
          <Box className={`dropdown-menu ${menuOpen ? 'open' : ''}`} sx={{ zIndex: 1300 }}>
            <FormControl fullWidth margin="normal">
              <InputLabel>Language</InputLabel>
              <Select defaultValue="">
                <MenuItem value="English">English</MenuItem>
                <MenuItem value="Vietnamese">Vietnamese</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
              <InputLabel>Voice</InputLabel>
              <Select defaultValue="">
                <MenuItem value="Male">Male</MenuItem>
                <MenuItem value="Female">Female</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
              <InputLabel>Gender</InputLabel>
              <Select defaultValue="">
                <MenuItem value="Male">Male</MenuItem>
                <MenuItem value="Female">Female</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth margin="normal">
              <InputLabel>Color</InputLabel>
              <Select value={themeProfile} onChange={handleThemeProfileChange}>
                <MenuItem value="tiramisu">Tiramisu</MenuItem>
                <MenuItem value="alpine">Alpine</MenuItem>
                <MenuItem value="dracula">Dracula</MenuItem>
                <MenuItem value="black-and-white">Black & White</MenuItem>
              </Select>
            </FormControl>
          </Box>
        )}
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 'calc(100vh - 64px)' }}>
          <Card sx={{ maxWidth: 345, mt: 8, zIndex: 1200 }}>
            <CardMedia component="img" height="140" image={placeholder} alt="Placeholder" />
          </Card>
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;

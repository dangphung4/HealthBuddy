import React, { useState, useEffect } from 'react';
import { NextUIProvider } from '@nextui-org/react';
import styled from '@emotion/styled';
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  NavbarMenuToggle,
  NavbarMenu,
  NavbarMenuItem,
  Link,
  Button,
} from '@nextui-org/react';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import './App.css';
import placeholder from './components/placeholder.png'; // Update the import path to match your project structure

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

const Header = styled.header`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 10px;
`;

const IconButton = styled.button`
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  color: var(--icon-color);

  &.icon-button {
    color: var(--icon-color);
  }

  &:hover, &:focus, &:active {
    background-color: transparent;
    color: var(--icon-color);
  }
`;

const Main = styled.main`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
`;

const ImageContainer = styled.div`
  width: 90vw;
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  overflow: hidden;
`;

const NavItem = styled(NavbarItem)`
  &:hover {
    background-color: var(--nav-item-hover);
  }
`;

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    document.body.classList.toggle('dark-mode', darkMode);
    document.body.classList.toggle('light-mode', !darkMode);
  }, [darkMode]);

  const menuItems = ['Home', 'Other', 'Settings', 'Log Out'];

  return (
    <NextUIProvider>
      <Container>
        <Navbar onMenuOpenChange={setIsMenuOpen} className="navbar" isBordered>
          <NavbarContent justify="center">
            <NavbarMenuToggle
              aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
              className="sm:hidden"
            />
            <NavbarBrand>
              <p className="font-bold text-inherit">HealthBuddy</p>
            </NavbarBrand>
          </NavbarContent>
          <NavbarContent className="hidden sm:flex gap-4" justify="center">
            <NavItem className="nav-item">
              <Link color="foreground" href="#">
                Home
              </Link>
            </NavItem>
            <NavItem className="nav-item">
              <Link color="foreground" href="#">
                Settings
              </Link>
            </NavItem>
          </NavbarContent>
          <NavbarContent justify="end">
            <NavbarItem className="nav-item">
              <IconButton onClick={() => setDarkMode(!darkMode)} className="icon-button">
                {darkMode ? <DarkModeIcon /> : <LightModeIcon />}
              </IconButton>
            </NavbarItem>
            <NavbarItem className="nav-item hidden lg:flex">
              <Link href="#">Login</Link>
            </NavbarItem>
          </NavbarContent>
          <NavbarMenu>
            {menuItems.map((item, index) => (
              <NavbarMenuItem key={`${item}-${index}`}>
                <Link
                  color={
                    index === 2 ? 'primary' : index === menuItems.length - 1 ? 'danger' : 'foreground'
                  }
                  className="w-full"
                  href="#"
                  size="lg"
                >
                  {item}
                </Link>
              </NavbarMenuItem>
            ))}
          </NavbarMenu>
        </Navbar>
        <Main>
          <ImageContainer>
            <img src={placeholder} alt="Sample" style={{ width: '100%', height: 'auto' }} />
          </ImageContainer>
        </Main>
      </Container>
    </NextUIProvider>
  );
};

export default App;

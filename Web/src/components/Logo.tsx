import React from 'react';
import styled from '@emotion/styled';

const LogoImage = styled.img`
  height: 40px;
  width: auto;
`;

const Logo: React.FC = () => {
  return <LogoImage src="/path-to-your-logo.png" alt="Logo" />;
};

export default Logo;
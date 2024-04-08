import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserId } from '../../utils/auth';
import Page from '../../components/layout/Page';

const RedirectProfilePage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    navigate(`/profile/${getUserId()}`);  
  }, [ navigate ]);
  return <Page>
    <div></div>
  </Page>;
};

export default RedirectProfilePage;
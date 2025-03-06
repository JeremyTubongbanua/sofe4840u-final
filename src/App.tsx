import logo from './logo.svg';
import './App.css';
import Account from "./Account.tsx"
import Register from './Register.tsx';
import Main from './Main.tsx';
import { BrowserRouter, Route, Routes, useRoutes } from 'react-router-dom';

const AppRoutes = () => {
  return useRoutes([
    { path: "/", element: <Main /> },
    { path: "/a", element: <Account /> },
    { path: "/r", element: <Register /> }
  ]);
};

function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}

export default App;

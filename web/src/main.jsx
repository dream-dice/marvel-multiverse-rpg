import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Login from './Login.jsx';
import 'bulma/css/bulma.css'

import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
  },
  {
    path: '/login',
    element: <Login />,
  }
], {
  basename: '/web'
});

ReactDOM.createRoot(document.getElementById('root')).render(<RouterProvider router={router} />)

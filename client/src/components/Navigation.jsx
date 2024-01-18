import { Link, useLocation } from 'react-router-dom';
import logoImage from './logo.png';

export function Navigation() {
  const location = useLocation();

  const buttonStyleCreate = {
    height: location.pathname === '/create' ? '2.5rem' : '3rem',
  };

  const buttonStyleHistory = {
    height: '3rem',
    marginTop: '35px', // Agregamos un margen superior de 10px
  };

  return (
    <div className='flex justify-between py-3'>
      <Link to='/create'>
        <img src={logoImage} alt='Logo' style={{ height: '125px', width: 'auto' }} />
      </Link>
      {location.pathname === '/create' ? (
        <button
          className='bg-violet-500 hover:bg-violet-700 px-3 py-2 rounded-lg'
          style={buttonStyleHistory} // Usamos el estilo del botón "Historial"
        >
          <Link to='/history'>Historial</Link>
        </button>
      ) : (
        <button
          className='bg-violet-500 hover:bg-violet-700 px-3 py-2 rounded-lg'
          style={buttonStyleHistory} // Usamos el estilo dinámico para el botón "Crear Regla"
        >
          <Link to='/create'>Crear Regla</Link>
        </button>
      )}
    </div>
  );
}
import React, { useState } from 'react';
import axios from 'axios';
import * as FaIcons from 'react-icons/fa';
import * as AiIcons from 'react-icons/ai';
import { Link } from 'react-router-dom';
import { LoggedInOptions, LoggedOutOptions } from '../home/SidebarData';
import './Navbar.css';
import { IconContext } from 'react-icons';
import {useStateValue} from '../Context/StateProvider'

function Navbar() {

  const [sidebar, setSidebar] = useState(false);

  const showSidebar = (() => {
    setSidebar(!sidebar);
  })
  const [{user}, dispatch] = useStateValue()

  var sidebarData = LoggedOutOptions
  if (user) {
    sidebarData = LoggedInOptions
  }

  return (
    <>
      <IconContext.Provider value={{ color: 'black' }}>
        <div className='navbar'>
          <Link to='#' className={sidebar ? 'menu-bars active' : 'menu-bars'}>
            <FaIcons.FaBars onClick={showSidebar} />
          </Link>
        </div>
        </IconContext.Provider>
        <IconContext.Provider value={{color:'white'}}>
        <nav className={sidebar ? 'nav-menu active' : 'nav-menu'}>
          <ul className='nav-menu-items' onClick={showSidebar}>
            <li className='navbar-toggle'>
              <Link to='#' className={sidebar ? 'menu-x active' : 'menu-x'}>
                <AiIcons.AiOutlineClose />
              </Link>
            </li>
            {sidebarData.map((item, index) => {
              return (
                <li key={index} className={item.cName}>
                  <Link to={item.path}>
                    {item.icon}
                    <span>{item.title}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </IconContext.Provider>
    </>
  );
}

export default Navbar;
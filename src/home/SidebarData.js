import React from 'react';
import * as AiIcons from 'react-icons/ai';
import * as MdIcons from 'react-icons/md';
import * as FaIcons from 'react-icons/fa';
export const LoggedOutOptions= [
  {
    title: 'Home',
    path: '/',
    icon: <AiIcons.AiFillHome />,
    cName: 'nav-text'
  },
  {
    title: 'Sign In',
    path: '/login',
    icon: <MdIcons.MdAccountCircle />,
    cName: 'nav-text'
  },
];

export const LoggedInOptions = [
  {
    title: 'Home',
    path: '/',
    icon: <AiIcons.AiFillHome />,
    cName: 'nav-text'
  },
  {
    title: 'Events',
    path: '/events',
    icon: <FaIcons.FaRegCalendarAlt />,
    cName: 'nav-text'
  },
  {
    title: 'Sign Out',
    path: '/logout',
    icon: <MdIcons.MdAccountCircle />,
    cName: 'nav-text'
  },
]
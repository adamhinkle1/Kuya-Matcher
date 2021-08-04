import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import { Link } from 'react-router-dom';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Typography from '@material-ui/core/Typography';
import { Collapse } from '@material-ui/core';

const useStyles = makeStyles({
  link: {
    textDecoration: 'none',
  },
  card: {
    minWidth: '80vh',
    background: 'rgba(0,0,0,0.25)',
    margin: '50px',
    borderRadius: '10px',
    boxShadow: '1px 1px 10px 1px rgba(0,0,0,.5), -1px -1px 10px 1px rgba(0,0,0,.5)',
    transition: 'transform 0.2s ease',
    '&:hover': {
      transform: 'scale(1.01)',
    },
  },
  media: {
    height: 440,
  },
  title: {
    fontFamily: 'Nunito',
    fontWeight: 'bold',
    fontSize: '2rem',
    color: '#fff',
  },
  desc: {
    fontFamily: 'Nunito',
    fontSize: '1.1rem',
    color: '#ddd',
  },
});

export default function ImageCard({ place, checked }) {
  const classes = useStyles();
  return (
    <Collapse in={checked} {...(checked ? { timeout: 1000 } : {})}>
      <Link to={place.path} className={classes.link}>
        <Card className={classes.card}>
          <CardMedia
            className={classes.media}
            image={place.imageUrl}
            title="Contemplative Reptile"
          />
          <CardContent>
            <Typography
              gutterBottom
              variant="h5"
              component="h1"
              className={classes.title}
            >
              {place.title}
            </Typography>
          </CardContent>
        </Card>
      </Link>
    </Collapse>
  );
}
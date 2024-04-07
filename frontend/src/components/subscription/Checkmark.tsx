import { ReactComponent as Checkmark } from 'bootstrap-icons/icons/patch-check-fill.svg';
import React from 'react';
import { Link } from 'react-router-dom';


export default function SubscriptionCheckmark({ style } : { style?: React.CSSProperties }) {
  return <Link to={"/subscription"}><Checkmark style={{
    height: "100%",
    width: "100%",
    color: "cyan",
    ...style
  }} /></Link>;
}
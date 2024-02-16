// import React, { useState } from 'react';
// import { Offcanvas, Button } from 'react-bootstrap';
// import Footer from './Footer';
// import Navigation from './Navigation';

// const Page = ({ children }:  { children: React.ReactNode }) => {
//     const [showSidebar, setShowSidebar] = useState(false);

//     const handleClose = () => setShowSidebar(false);
//     const handleShow = () => setShowSidebar(true);

//     return (
//         <div>
//             <div>
//                 <Navigation items={[
//                     { name: "Home", icon: "home", path: "/home" },
//                     { name: "Profile", icon: "profile", path: "/profile" },
//                     { name: "Network", icon: "network", path: "/network" },
//                     { name: "Settings", icon: "settings", path: "/settings" }
//                 ]} />
//                 <Button variant="primary" onClick={handleShow}>
//                     Toggle Sidebar
//                 </Button>
//             </div>
//             <div>
//                 {children}
//             </div>

//             <Offcanvas show={showSidebar} onHide={handleClose} placement="end">
//                 <Offcanvas.Header closeButton>
//                     <Offcanvas.Title>Sidebar Title</Offcanvas.Title>
//                 </Offcanvas.Header>
//                 <Offcanvas.Body>
//                     {/* Your sidebar content goes here */}
//                     <p>Your Sidebar Content Here</p>
//                 </Offcanvas.Body>
//             </Offcanvas>


//             <Footer />
//         </div>
//     );
// };

// export default Page;


import React, { useState } from "react";
import styles from "./Page.module.css";
import Footer from "./Footer";
import { Offcanvas, Button } from 'react-bootstrap';
import Inbox from "../inbox/Inbox";
import Navigation from "./Navigation";

const Page = ({ children } : { children: React.ReactNode }) => {
    
    
    const [showSidebar, setShowSidebar] = useState(false);
    const toggleSidebar = () => setShowSidebar(!showSidebar);
    
    return (
        <div id={styles.root}>

            <div id={styles.contentRoot}>
                <div id={styles.navigation}>
                    <Navigation items={[
                        { name: "Home", icon: "home", path: "/home" },
                        { name: "Profile", icon: "profile", path: "/profile" },
                        { name: "Network", icon: "network", path: "/network" },
                        { name: "Settings", icon: "settings", path: "/settings" }
                    ]} />
                </div>
                <div id={styles.content}>
                    <div id={styles.thinNavbar}>
                        <button onClick={() => {toggleSidebar()}}>Inbox</button>
                        <button onClick={() => {/* TODO: Handle sign out */}}>Sign Out</button>
                    </div>
                    {children}
                </div>
            </div>
            <Offcanvas show={showSidebar} onHide={() => {setShowSidebar(false);}} placement="end">
                <Offcanvas.Header closeButton>
                    <Offcanvas.Title>Inbox</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body>
                    <Inbox></Inbox>
                </Offcanvas.Body>
            </Offcanvas>
            <Footer />
        </div>
    );
};

export default Page;
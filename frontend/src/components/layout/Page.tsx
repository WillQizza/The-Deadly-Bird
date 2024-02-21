import React, { useState } from "react";
import styles from "./Page.module.css";
import Footer from "./Footer";
import { Offcanvas } from 'react-bootstrap';
import Inbox from "../inbox/Inbox";
import Navigation, { SelectedNavigation } from "./Navigation";
import { useNavigate } from "react-router-dom";

const Page = ({ children, selected } : { children: React.ReactNode, selected?: SelectedNavigation }) => {
        
    const [showSidebar, setShowSidebar] = useState(false);
    const toggleSidebar = () => setShowSidebar(!showSidebar);
    let navigate = useNavigate();

    const logOut = () => {
        // TODO: Handle logout
        navigate("/");
    };

    return (
        <div id={styles.root}>

            <div id={styles.contentRoot}>
                <div id={styles.navigation}>
                    <Navigation items={[
                        { name: "Home", icon: "home", path: "/home" },
                        { name: "Profile", icon: "profile", path: "/profile" },
                        { name: "Network", icon: "network", path: "/network" },
                        { name: "Settings", icon: "settings", path: "/profile/settings" }
                    ]} selected={selected} />
                </div>
                <div id={styles.contentAndUpperNav}>
                    <div id={styles.thinNavbar}>
                        <button onClick={() => {toggleSidebar()}}>Inbox</button>
                        <button onClick={() => {logOut()}}>Log Out</button>
                    </div>
                    <div id={styles.content}>
                        {children}
                    </div>
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